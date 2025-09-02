from ..BaseMetaDataInferenceHandler import MetaDataInferenceHandler
from ....models.Task import QueryTaskMaterial
import logging

from sqlglot import parse_one, Expression, exp
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.annotate_types import annotate_types
from sqlglot.optimizer.scope import (
    build_scope,
    find_all_in_scope,
    traverse_scope,
    Scope,
)
from enum import Enum, auto
from typing import List
import re


class QueryMetricsHandler(MetaDataInferenceHandler):
    """
    Currently wraps the SQLGlot-library and uses its parser to calculate basic counting metrics.
    """
    def __init__(self):
        super().__init__()
        self._analyzer = SQLAnalyzer()

    def infer_metadata(self, query_material: QueryTaskMaterial):
        query = query_material.query
        dialect = query_material.dialect

        # result = self._analyzer.analyze_query(query, dialect)

        return {
            # "test": 1
        }



# type SchemaInformation = dict[str, str | SchemaInformation]
# TODO: Externalize the code below into its own package => SHK/WHK FeU

class ScopeType(Enum):
    ROOT = auto()
    SUBQUERY = auto()
    CORRELATED_SUBQUERY = auto()
    DERIVED_TABLE = auto()
    CTE = auto()
    UNION = auto()
    UDTF = auto()
    UNKNOWN = auto()

class SQLAnalyzer:
    def __init__(self):
        self._parser = parse_one
        self._scope_handlers = {
            ScopeType.ROOT: self._analyze_columns
        }

    def _substitute_newline_and_tabs(self, s: str) -> str:
        return " ".join(s.split())
    
    def _clean_query_string(self, query: str) -> str:
        return self._substitute_newline_and_tabs(query)

    def _extract_selected_column_string(self, query: str) -> str:
        single_line_query = self._clean_query_string(query)

        match = re.search(r"SELECT (.*?) FROM", single_line_query, flags=re.IGNORECASE)
        if match:
            return match.groups()[0]
        return ""


    def _qualify_and_annotate_ast(self, ast: Expression, schema_information: dict):
        if schema_information:
            qualified_ast = qualify(ast, schema=schema_information)
            annotated_qualified_ast = annotate_types(qualified_ast, schema=schema_information)
            return annotated_qualified_ast

        return ast

    def _assemble_query_scopes(self, ast: Expression):
        return build_scope(ast)
    
    def _determine_scope_type(self, scope: Scope) -> ScopeType:
        if scope.is_correlated_subquery:
            return ScopeType.CORRELATED_SUBQUERY
        elif scope.is_cte:
            return ScopeType.CTE
        elif scope.is_derived_table:
            return ScopeType.DERIVED_TABLE
        elif scope.is_subquery:
            return ScopeType.SUBQUERY
        elif scope.is_udtf:
            return ScopeType.UDTF
        elif scope.is_union:
            return ScopeType.UNION
        # Check for root last. Important, as e.g. UNION or CTE could be ROOT as well.
        # => Base-case is the SELECT-Statement. UNION or CTE might be root also,
        elif scope.is_root:
            return ScopeType.ROOT
        else:
            return ScopeType.UNKNOWN
    
    
    def _iterate_query_scopes(self, scopes: List[Scope]):
        # top_down_scopes = traverse_scope(scopes).reverse()
        top_down_scopes = [scopes]
        for query_scope in top_down_scopes:
            scope_type = self._determine_scope_type(query_scope)
            self._scope_handlers[scope_type](query_scope)
            # query_scope.expression.sql()


    def _analyze_columns(self, scope: Scope):
        # query = ast.sql(dialect=self.dialect)
        column_string = self._extract_selected_column_string(scope.expression)
        column_ast = self.parser(column_string)
        
        logging.getLogger('uvicorn.error').info("STUFF")
        logging.getLogger().debug(column_ast.find_all(exp.AggFunc))

        return column_ast.find_all(exp.AggFunc)


    def analyze_query(self, query: str, dialect: str = "postgres", schema_information: dict = None):
        # cleaned_query = self._clean_query_string(query)
        ast = self._parser(sql=query, dialect=dialect)
        qualified_ast = self._qualify_and_annotate_ast(ast, schema_information)

        query_scopes = self._assemble_query_scopes(qualified_ast)

        self._iterate_query_scopes(query_scopes)

        qualified_ast