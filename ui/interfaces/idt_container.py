from typing import Any, Dict

from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtCore import QTimer, Qt

DEBOUNCE_INTERVAL = 500


class IDTContainer:
    def init_interface(self) -> None:
        self._children: Dict[str, IDTContainer] = {}
        self._components: Dict[str, Any] = {}
        self._debounce_timer = QTimer(self)
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.timeout.connect(self._emit_values_changed)

    def add_child(self, name: str, child: "IDTContainer", alignment: Qt.AlignmentFlag = None) -> None:
        self._children[name] = child
        self._components[name] = child
        self._connect_component_signals(child)
        if alignment is None:
            self.main_layout.addWidget(child)
        else:
            self.main_layout.addWidget(child, alignment)
        child.values_changed.connect(lambda values: self._handle_child_values_changed(name, values))

    def add_component(self, name: str, component: Any) -> None:
        self._components[name] = component
        self._connect_component_signals(component)
        self.main_layout.addWidget(component)

    def _connect_component_signals(self, component: Any) -> None:
        signal_mappings = {
            'textChanged': self._on_values_changed,
            'currentTextChanged': self._on_values_changed,
            'stateChanged': self._on_values_changed,
            'value_changed': self._on_values_changed,
            'values_changed': self._on_values_changed
        }
        for signal_name, handler in signal_mappings.items():
            if hasattr(component, signal_name):
                getattr(component, signal_name).connect(lambda *args, h=handler: h())

    def _on_values_changed(self) -> None:
        self._debounce_timer.start(DEBOUNCE_INTERVAL)

    def _emit_values_changed(self) -> None:
        values = self.get_values()
        self.values_changed.emit(values)

    def update_component_value(self, name: str, value: Any) -> None:
        if name not in self._components:
            return
        component = self._components[name]
        self._set_component_value(component, value)

    def update_components_from_values(self, values: dict) -> None:
        for name, value in values.items():
            self.update_component_value(name, value)

    def _set_component_value(self, component: Any, value: Any) -> None:
        method_mappings = {
            'setText': str,
            'setCurrentText': str,
            'setChecked': bool,
            'set_value': lambda x: x,
            'set_values': lambda x: x
        }
        for method_name, converter in method_mappings.items():
            if hasattr(component, method_name):
                try:
                    getattr(component, method_name)(converter(value))
                    break
                except (ValueError, TypeError):
                    continue

    def get_component_value(self, name: str) -> Any:
        if name not in self._components:
            return None
        component = self._components[name]
        return self._get_component_value(component)

    def _get_component_value(self, component: Any) -> Any:
        try:
            if hasattr(component, 'text'):
                if isinstance(component, QCheckBox):
                    return component.isChecked()
                return component.text()
            elif hasattr(component, 'currentText'):
                return component.currentText()
            elif hasattr(component, 'isChecked'):
                return component.isChecked()
            elif hasattr(component, 'get_values'):
                return component.get_values()
            elif hasattr(component, 'get_value'):
                return component.get_value()
            return None
        except RuntimeError:
            return None

    def get_values(self) -> Dict[str, Any]:
        return {name: self.get_component_value(name) for name in self._components}

    def _handle_child_values_changed(self, child_name: str, child_values: dict) -> None:
        all_values = self.get_values()
        self.values_changed.emit(all_values)
