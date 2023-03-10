from typing import Optional, List

from pydantic import BaseModel


class CommitUrlinfo(BaseModel):
    name: str
    url: str
    type: str
    description: str
    tags: List


class CommitCalendar(BaseModel):
    name: str
    date: str


class CommitInform(BaseModel):
    title: str
    date: str
    detail: str
    type: int
