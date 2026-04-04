from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QWidget


class AttendanceChartWidget(QWidget):
    """
    Mini chart vẽ bằng QPainter (thay thế tương đương cho chart lib).
    Hiển thị xu hướng điểm danh 7 ngày gần nhất.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.labels: list[str] = []
        self.values: list[int] = []
        self.setMinimumHeight(220)

    def set_data(self, labels: list[str], values: list[int]):
        self.labels = labels
        self.values = values
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(16, 16, -16, -24)
        painter.fillRect(self.rect(), Qt.transparent)

        if not self.values:
            painter.setPen(QColor("#94A3B8"))
            painter.drawText(rect, Qt.AlignCenter, "Chua co du lieu attendance")
            return

        max_value = max(self.values) if max(self.values) > 0 else 1
        count = len(self.values)

        # Vẽ lưới nền nhẹ để dễ đọc biểu đồ.
        grid_pen = QPen(QColor("#1E293B"), 1)
        painter.setPen(grid_pen)
        for i in range(1, 4):
            y = rect.top() + i * rect.height() / 4
            painter.drawLine(rect.left(), int(y), rect.right(), int(y))

        step_x = rect.width() / max(count - 1, 1)
        points = []
        for idx, value in enumerate(self.values):
            x = rect.left() + idx * step_x
            y_ratio = value / max_value
            y = rect.bottom() - (rect.height() * 0.75 * y_ratio)
            points.append(QPointF(x, y))

        if len(points) >= 2:
            area_path = QPainterPath()
            area_path.moveTo(points[0])
            for p in points[1:]:
                area_path.lineTo(p)
            area_path.lineTo(QPointF(points[-1].x(), rect.bottom()))
            area_path.lineTo(QPointF(points[0].x(), rect.bottom()))
            area_path.closeSubpath()
            painter.fillPath(area_path, QColor(59, 130, 246, 55))

        line_pen = QPen(QColor("#60A5FA"), 3)
        painter.setPen(line_pen)
        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])

        dot_pen = QPen(QColor("#93C5FD"), 1)
        painter.setPen(dot_pen)
        painter.setBrush(QColor("#60A5FA"))
        for p in points:
            painter.drawEllipse(p, 4, 4)

        label_font = QFont("Segoe UI", 9)
        painter.setFont(label_font)
        painter.setPen(QColor("#CBD5E1"))

        for i, p in enumerate(points):
            painter.drawText(int(p.x() - 10), rect.bottom() + 18, self.labels[i])
            painter.drawText(int(p.x() - 8), int(p.y() - 10), str(self.values[i]))
