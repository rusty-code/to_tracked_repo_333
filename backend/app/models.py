from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Op = Literal["==", "!=", ">", "<", ">=", "<="]


class Signal(BaseModel):
    name: str
    title: str = ""
    type: str = ""
    unit: str = ""
    values: dict[str, str] = {}  # для списка значений: {"0": "нет", "1": "протечка"}
    alarm: str = ""  # тревожное значение списка, подсвечивается красным


class Event(BaseModel):
    name: str
    title: str = ""
    when: dict[str, Any] = {}  # событие наступает, когда сигналы стали равны этим значениям


class Command(BaseModel):
    name: str
    title: str = ""
    set: dict[str, Any] = {}  # какие сигналы меняет команда; "$value" — значение из запроса


class Setting(BaseModel):
    name: str
    title: str = ""
    unit: str = ""
    value: float = 0
    min: float = 0
    max: float = 100


class Device(BaseModel):
    id: str
    title: str
    room: str = ""
    type: str = ""
    section: str = ""  # service — служебное окно, vet — ветеринары
    ujin_ext: str = ""
    signals: list[Signal] = []
    events: list[Event] = []
    commands: list[Command] = []
    settings: list[Setting] = []
    online: bool = True
    state: dict[str, Any] = {}
    updated: str = ""


class When(BaseModel):
    type: Literal["event", "signal", "manual"]
    device: str = ""
    event: str = ""
    signal: str = ""
    op: Op = "=="
    value: Any = None


class If(BaseModel):
    device: str
    signal: str
    op: Op = "=="
    value: Any = None


class Then(BaseModel):
    type: Literal["command", "notify"]
    device: str = ""
    command: str = ""
    value: Any = None
    to: str = "service"
    text: str = ""


class Scenario(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = ""
    title: str
    enabled: bool = True
    when: When
    if_: list[If] = Field([], alias="if")
    then: list[Then] = []
    last_run: str = ""
    last_result: str = ""
