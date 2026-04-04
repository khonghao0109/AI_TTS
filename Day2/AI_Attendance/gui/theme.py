"""
Theme dùng chung cho toàn bộ giao diện.
Phong cách Dark SaaS với card bo góc và sidebar hiện đại.
"""

APP_STYLESHEET = """
QMainWindow {
    background-color: #0F172A;
}

QWidget {
    color: #E2E8F0;
    font-family: "Montserrat", "Roboto", "Segoe UI";
    font-size: 13px;
    background: transparent;
}

QFrame#Card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 16px;
}

QFrame#SidebarPanel {
    background: #020617;
    border: 1px solid #1F2937;
    border-radius: 18px;
}

QPushButton#NavButton {
    text-align: left;
    color: #CBD5E1;
    border: none;
    border-radius: 12px;
    padding: 10px 12px;
    font-weight: 600;
}

QPushButton#NavButton:hover {
    background: rgba(96, 165, 250, 0.16);
}

QPushButton#NavButton:checked {
    background: #1D4ED8;
    color: #F8FAFC;
}

QPushButton#PrimaryButton {
    background: #2563EB;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 14px;
    font-weight: 700;
}

QPushButton#PrimaryButton:hover {
    background: #1D4ED8;
}

QPushButton#DangerButton {
    background: #DC2626;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 14px;
    font-weight: 700;
}

QPushButton#DangerButton:hover {
    background: #B91C1C;
}

QPushButton#GhostButton {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 9px 12px;
    color: #E2E8F0;
}

QLineEdit, QComboBox {
    background: #0B1220;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 8px 10px;
    color: #E2E8F0;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #3B82F6;
}

QTableWidget {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 12px;
    gridline-color: #1F2937;
    color: #E2E8F0;
}

QHeaderView::section {
    background: #0B1220;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #334155;
    font-weight: 700;
    color: #CBD5E1;
}

QListWidget {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 12px;
    color: #E2E8F0;
}
"""
