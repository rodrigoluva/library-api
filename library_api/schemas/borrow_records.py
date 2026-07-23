from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class BorrowRecordPublicSchema(BaseModel):
    id: int
    user_id: int
    book_copy_id: int
    borrowed_at: datetime
    due_at: datetime
    returned_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class BorrowRecordListSchema(BaseModel):
    borrow_records: List[BorrowRecordPublicSchema]
    offset: int
    limit: int
