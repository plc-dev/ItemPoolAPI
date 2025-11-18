from .BaseTaskMaterial import (
    TaskMaterial,
    Metadata,
    TaskMaterialRegistrationRequestObject,
    MaterialType,
)


class TextMetadata(Metadata):
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    smog_index: float
    coleman_liau_index: float
    automated_readability_index: float
    dale_chall_readability_score: float
    difficult_words: float
    linsear_write_formula: float
    gunning_fog: float
    text_standard: float
    fernandez_huerta: float
    szigriszt_pazos: float
    gutierrez_polini: float
    crawford: float
    gulpease_index: float
    osman: float


class TextTaskMaterial(TaskMaterial):
    text: str


class TextMaterialRegistrationRequestObject(TaskMaterialRegistrationRequestObject):
    type: MaterialType.text
    material_information: TextTaskMaterial
