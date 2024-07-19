import datetime
import json
from typing import List, Optional

from core.db.mysql import MySqlConnector
from pydantic import BaseModel, root_validator, Field, validator


class LogMessage(BaseModel):
    create_date:    Optional[datetime.datetime] = None
    update_date:    Optional[datetime.datetime] = None
    interval:       Optional[int] = Field(None, description='Interval in seconds')
    dialog_id:      Optional[str] = None
    prompt:         Optional[str] = Field(None, alias="name")
    message:        Optional[List[dict]] = None
    reference:      Optional[list] = None

    @root_validator(pre=True)
    def set_interval(cls, values):
        create_dt = values.get('create_date')
        update_dt = values.get('update_date')
        if create_dt and update_dt:
            values['interval'] = (update_dt - create_dt).total_seconds()
        return values

    @validator('message', 'reference', pre=True)
    def parse_message(cls, value):
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                raise ValueError('Invalid JSON format for message')
        return value


class LogRetriever:
    def __init__(self):
        self.connector = MySqlConnector()
        self.connector.connect()
        self.sql = r"""
        select create_date, update_date, dialog_id, name, message, reference
        from conversation
        where DATE(create_date) = DATE(%s);
        """

    def get_log_at_date(self,
                        date: datetime.date = datetime.date.today()) -> List[LogMessage]:
        _messages = self.connector.execute_sql(self.sql,
                                               (date.strftime('%Y-%m-%d'), ),
                                               fetch=True,
                                               fetch_all=True)
        messages = []
        for _message in _messages:
            _message = LogMessage.model_validate(_message)
            messages.append(_message)
        return messages


if __name__ == '__main__':
    lr = LogRetriever()
    result = lr.get_log_at_date()
    print(result[0])
