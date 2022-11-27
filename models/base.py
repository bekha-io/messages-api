from pydantic import *


class Model(BaseModel):
    class Config:
        extra = "allow"  # For non-export auto-generated fields that should not be shown in docs.
        # Exclude does not meet our requirements in this case
