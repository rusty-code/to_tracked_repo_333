from __future__ import annotations

from core import Device, Signal

MODERATELY, STRONG = 0, 1

class Filter(Device):
    model = "emul_filter"
    title = "Фильтр"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pH = 8.2
        self.add_signal(Signal("pH", "Кислотность", "graph", "property", 8.2))
        self.add_signal(Signal("haze", "мутность", "list", "r", "property", 0,
                               layout={0:"нет", 1:"есть"}))
        self.add_signal(Signal("mode", "Режим", "list", "rw", "capability", MODERATELY,
                               layout={MODERATELY:"умеренная фильтрация", STRONG:"усиленная фильтрация"}))
        self.add_signal(Signal("battery", "Батарея", "graph", "r", "property", 100, "%"))
        self.add_signal(Signal("self_test", "Самотест", "button", "w", "capability", 0))

    def _set_pH(self, level: float):
        self._pH = max(0.0, min(14.0, level))

    def tick(self, dt: int) -> None:
        self.set_value("pH", self._pH)
        pH_bad = ((self._pH < 8.0) or (self._pH > 8.5))
        haze_bad = self.signals["haze"].value == 1
        if pH_bad or haze_bad:
            self.set_value("mode", STRONG)
        else:
            self.set_value("mode", MODERATELY)