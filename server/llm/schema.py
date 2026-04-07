from pydantic import BaseModel, Field
from typing import List, Literal, Optional

class Preprocess_steps(BaseModel):
    step: Literal['Impute','SMOTE','Scale','One_Hot','Transform','Encode','Drop','Skip'] = Field(description='choose one of the given option to perform on the column')
    columns: Optional[List[str]] = Field(description='choose the columns to perform the chosen preprocessing step on')
    method: Optional[Literal['mean','median','mode','log','standard','minmax']] = Field(description='mention the type of step if required. eg- if step is chosen Impute then method can be mean,median,mode')

class Plan(BaseModel):
    steps: List[Preprocess_steps]