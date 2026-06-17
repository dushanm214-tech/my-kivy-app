"""
Apparel Production Planning App
Built with Python Kivy + KivyMD
"""

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.list import OneLineListItem
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
import datetime

# ─────────────────────────────────────────────
#  KV Layout String
# ─────────────────────────────────────────────
KV = """
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import MDSpinner kivymd.uix.spinner.MDSpinner

<RootScreen>:
    name: "root"
    md_bg_color: app.theme_cls.bg_darkest

    MDBoxLayout:
        orientation: "vertical"
        spacing: 0

        # ── HEADER ──────────────────────────────
        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: dp(130)
            padding: [dp(20), dp(16), dp(20), dp(10)]
            md_bg_color: get_color_from_hex("#1A237E")

            MDBoxLayout:
                orientation: "horizontal"
                size_hint_y: None
                height: dp(28)

                MDLabel:
                    text: "✂  APPAREL PLANNER"
                    font_style: "Caption"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#90CAF9")
                    bold: True
                    size_hint_x: 1

                MDLabel:
                    id: clock_label
                    text: ""
                    font_style: "Caption"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#90CAF9")
                    halign: "right"
                    size_hint_x: None
                    width: dp(90)

            MDLabel:
                text: "Production Planning"
                font_style: "H5"
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#FFFFFF")
                bold: True
                size_hint_y: None
                height: dp(40)

            MDBoxLayout:
                orientation: "horizontal"
                size_hint_y: None
                height: dp(32)
                spacing: dp(8)

                # Month pill
                MDCard:
                    id: month_pill
                    radius: [dp(14)]
                    md_bg_color: get_color_from_hex("#283593")
                    size_hint_x: None
                    width: dp(130)
                    on_release: app.show_month_picker()
                    ripple_behavior: True
                    elevation: 0

                    MDBoxLayout:
                        padding: [dp(10), 0]
                        MDLabel:
                            id: month_label
                            text: "📅  Select Month"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#BBDEFB")
                            halign: "center"

                MDCard:
                    radius: [dp(14)]
                    md_bg_color: get_color_from_hex("#283593")
                    size_hint_x: None
                    width: dp(110)
                    on_release: app.show_year_picker()
                    ripple_behavior: True
                    elevation: 0

                    MDBoxLayout:
                        padding: [dp(10), 0]
                        MDLabel:
                            id: year_label
                            text: "🗓  Year"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#BBDEFB")
                            halign: "center"

        # ── SCROLLABLE BODY ──────────────────────
        ScrollView:
            do_scroll_x: False

            MDBoxLayout:
                orientation: "vertical"
                padding: [dp(14), dp(12), dp(14), dp(20)]
                spacing: dp(12)
                adaptive_height: True

                # ── INPUT SECTION ────────────────
                MDCard:
                    radius: [dp(16)]
                    elevation: 2
                    md_bg_color: get_color_from_hex("#1E2A5E")
                    padding: dp(16)
                    spacing: dp(10)
                    adaptive_height: True
                    orientation: "vertical"

                    MDLabel:
                        text: "⚙  Factory Inputs"
                        font_style: "Subtitle1"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#82B1FF")
                        bold: True
                        size_hint_y: None
                        height: dp(28)

                    MDTextField:
                        id: mo_field
                        hint_text: "Number of Machines (MO)"
                        helper_text: "Total sewing machines in factory"
                        helper_text_mode: "on_focus"
                        input_filter: "float"
                        mode: "rectangle"
                        line_color_normal: get_color_from_hex("#3949AB")
                        line_color_focus: get_color_from_hex("#82B1FF")
                        hint_text_color_normal: get_color_from_hex("#7986CB")
                        text_color_normal: get_color_from_hex("#FFFFFF")
                        icon_left: "sewing-machine"
                        on_text: app.calculate()

                    MDTextField:
                        id: workhour_field
                        hint_text: "Work Hours per Day"
                        helper_text: "Daily operational hours"
                        helper_text_mode: "on_focus"
                        input_filter: "float"
                        mode: "rectangle"
                        line_color_normal: get_color_from_hex("#3949AB")
                        line_color_focus: get_color_from_hex("#82B1FF")
                        hint_text_color_normal: get_color_from_hex("#7986CB")
                        text_color_normal: get_color_from_hex("#FFFFFF")
                        icon_left: "clock-outline"
                        on_text: app.calculate()

                    MDTextField:
                        id: workdays_field
                        hint_text: "Working Days in Month"
                        helper_text: "Number of production days"
                        helper_text_mode: "on_focus"
                        input_filter: "float"
                        mode: "rectangle"
                        line_color_normal: get_color_from_hex("#3949AB")
                        line_color_focus: get_color_from_hex("#82B1FF")
                        hint_text_color_normal: get_color_from_hex("#7986CB")
                        text_color_normal: get_color_from_hex("#FFFFFF")
                        icon_left: "calendar-check"
                        on_text: app.calculate()

                    MDTextField:
                        id: plan_sah_field
                        hint_text: "Plan SAH"
                        helper_text: "Planned Standard Allowed Hours"
                        helper_text_mode: "on_focus"
                        input_filter: "float"
                        mode: "rectangle"
                        line_color_normal: get_color_from_hex("#3949AB")
                        line_color_focus: get_color_from_hex("#82B1FF")
                        hint_text_color_normal: get_color_from_hex("#7986CB")
                        text_color_normal: get_color_from_hex("#FFFFFF")
                        icon_left: "chart-line"
                        on_text: app.calculate()

                    MDTextField:
                        id: daily_earn_field
                        hint_text: "Daily Earn SAH"
                        helper_text: "Actual SAH earned per day"
                        helper_text_mode: "on_focus"
                        input_filter: "float"
                        mode: "rectangle"
                        line_color_normal: get_color_from_hex("#3949AB")
                        line_color_focus: get_color_from_hex("#82B1FF")
                        hint_text_color_normal: get_color_from_hex("#7986CB")
                        text_color_normal: get_color_from_hex("#FFFFFF")
                        icon_left: "currency-usd"
                        on_text: app.calculate()

                # ── SAH METRICS ──────────────────
                MDLabel:
                    text: "📊  SAH Dashboard"
                    font_style: "Subtitle1"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#82B1FF")
                    bold: True
                    size_hint_y: None
                    height: dp(24)
                    padding_x: dp(4)

                # Row 1: Available & Loading
                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(110)

                    # Available SAH
                    MDCard:
                        id: avail_card
                        radius: [dp(16)]
                        elevation: 3
                        md_bg_color: get_color_from_hex("#0D47A1")
                        padding: dp(12)
                        orientation: "vertical"

                        MDLabel:
                            text: "AVAILABLE SAH"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#90CAF9")
                            bold: True
                            size_hint_y: None
                            height: dp(20)
                            halign: "center"

                        MDLabel:
                            id: avail_label
                            text: "—"
                            font_style: "H5"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FFFFFF")
                            bold: True
                            halign: "center"

                        MDLabel:
                            text: "hrs/month"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#64B5F6")
                            halign: "center"
                            size_hint_y: None
                            height: dp(18)

                    # Loading SAH
                    MDCard:
                        id: load_card
                        radius: [dp(16)]
                        elevation: 3
                        md_bg_color: get_color_from_hex("#1A237E")
                        padding: dp(12)
                        orientation: "vertical"

                        MDLabel:
                            text: "LOADING SAH"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#CE93D8")
                            bold: True
                            size_hint_y: None
                            height: dp(20)
                            halign: "center"

                        MDLabel:
                            id: load_label
                            text: "—"
                            font_style: "H5"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FFFFFF")
                            bold: True
                            halign: "center"

                        MDLabel:
                            text: "80% capacity"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#BA68C8")
                            halign: "center"
                            size_hint_y: None
                            height: dp(18)

                # ── EARN SAH (full width) ────────
                MDCard:
                    radius: [dp(16)]
                    elevation: 3
                    md_bg_color: get_color_from_hex("#004D40")
                    padding: dp(14)
                    size_hint_y: None
                    height: dp(90)
                    orientation: "vertical"

                    MDLabel:
                        text: "TOTAL EARN SAH  (Daily × Working Days)"
                        font_style: "Caption"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#80CBC4")
                        bold: True
                        size_hint_y: None
                        height: dp(20)
                        halign: "center"

                    MDLabel:
                        id: earn_label
                        text: "—"
                        font_style: "H4"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#A5D6A7")
                        bold: True
                        halign: "center"

                # ── VARIATION SECTION ────────────
                MDLabel:
                    text: "📈  Variations"
                    font_style: "Subtitle1"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#82B1FF")
                    bold: True
                    size_hint_y: None
                    height: dp(24)
                    padding_x: dp(4)

                # Variation 1: Earn vs Available
                MDCard:
                    radius: [dp(16)]
                    elevation: 2
                    md_bg_color: get_color_from_hex("#212121")
                    padding: [dp(14), dp(12)]
                    size_hint_y: None
                    height: dp(120)
                    orientation: "vertical"
                    spacing: dp(4)

                    MDLabel:
                        text: "Earn SAH  vs  Available SAH"
                        font_style: "Body2"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#BDBDBD")
                        bold: True
                        size_hint_y: None
                        height: dp(22)

                    MDBoxLayout:
                        orientation: "horizontal"
                        size_hint_y: None
                        height: dp(36)
                        spacing: dp(8)

                        MDLabel:
                            id: var1_label
                            text: "—"
                            font_style: "H5"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FFFFFF")
                            bold: True
                            size_hint_x: None
                            width: dp(120)

                        MDLabel:
                            id: var1_status
                            text: ""
                            font_style: "Body2"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#BDBDBD")
                            valign: "center"

                    # Progress bar background
                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(8)
                        radius: [dp(4)]
                        md_bg_color: get_color_from_hex("#333333")

                        MDCard:
                            id: var1_bar
                            radius: [dp(4)]
                            size_hint_x: 0
                            md_bg_color: get_color_from_hex("#42A5F5")
                            elevation: 0

                # Variation 2: Loading vs Earn
                MDCard:
                    radius: [dp(16)]
                    elevation: 2
                    md_bg_color: get_color_from_hex("#212121")
                    padding: [dp(14), dp(12)]
                    size_hint_y: None
                    height: dp(120)
                    orientation: "vertical"
                    spacing: dp(4)

                    MDLabel:
                        text: "Loading SAH  vs  Earn SAH"
                        font_style: "Body2"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#BDBDBD")
                        bold: True
                        size_hint_y: None
                        height: dp(22)

                    MDBoxLayout:
                        orientation: "horizontal"
                        size_hint_y: None
                        height: dp(36)
                        spacing: dp(8)

                        MDLabel:
                            id: var2_label
                            text: "—"
                            font_style: "H5"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#FFFFFF")
                            bold: True
                            size_hint_x: None
                            width: dp(120)

                        MDLabel:
                            id: var2_status
                            text: ""
                            font_style: "Body2"
                            theme_text_color: "Custom"
                            text_color: get_color_from_hex("#BDBDBD")
                            valign: "center"

                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(8)
                        radius: [dp(4)]
                        md_bg_color: get_color_from_hex("#333333")

                        MDCard:
                            id: var2_bar
                            radius: [dp(4)]
                            size_hint_x: 0
                            md_bg_color: get_color_from_hex("#AB47BC")
                            elevation: 0

                # ── PLAN SAH STATUS ─────────────
                MDCard:
                    radius: [dp(16)]
                    elevation: 2
                    md_bg_color: get_color_from_hex("#1B2838")
                    padding: dp(14)
                    size_hint_y: None
                    height: dp(80)
                    orientation: "vertical"
                    spacing: dp(4)

                    MDLabel:
                        text: "Plan SAH  vs  Earn SAH  (Achievement)"
                        font_style: "Body2"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#BDBDBD")
                        bold: True
                        size_hint_y: None
                        height: dp(22)

                    MDLabel:
                        id: plan_status_label
                        text: "—"
                        font_style: "Subtitle1"
                        theme_text_color: "Custom"
                        text_color: get_color_from_hex("#FFFFFF")
                        bold: True

                # ── RESET BUTTON ─────────────────
                MDRaisedButton:
                    text: "🔄  Reset All"
                    md_bg_color: get_color_from_hex("#B71C1C")
                    size_hint_x: 1
                    height: dp(48)
                    font_size: "15sp"
                    on_release: app.reset_all()
                    elevation: 4
"""


# ─────────────────────────────────────────────
#  Screen class
# ─────────────────────────────────────────────
class RootScreen(Screen):
    pass


# ─────────────────────────────────────────────
#  Main App
# ─────────────────────────────────────────────
class ApparelPlannerApp(MDApp):

    MONTHS = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    selected_month = StringProperty("Select Month")
    selected_year = StringProperty("")
    month_dialog = None
    year_dialog = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Indigo"

        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(RootScreen(name="root"))
        return sm

    def on_start(self):
        now = datetime.datetime.now()
        self.selected_month = self.MONTHS[now.month - 1]
        self.selected_year = str(now.year)
        self._update_month_label()
        Clock.schedule_interval(self._tick, 1)

    # ── Clock ─────────────────────────────────
    def _tick(self, dt):
        now = datetime.datetime.now()
        lbl = self.root.get_screen("root").ids.get("clock_label")
        if lbl:
            lbl.text = now.strftime("%H:%M:%S")

    # ── Month/Year display ────────────────────
    def _update_month_label(self):
        ids = self.root.get_screen("root").ids
        ids.month_label.text = f"📅  {self.selected_month[:3]}"
        ids.year_label.text = f"🗓  {self.selected_year}"

    # ── Month Picker ──────────────────────────
    def show_month_picker(self):
        items = [
            OneLineListItem(
                text=m,
                on_release=lambda x, month=m: self._pick_month(month)
            )
            for m in self.MONTHS
        ]
        self.month_dialog = MDDialog(
            title="Select Month",
            type="simple",
            items=items,
            buttons=[
                MDFlatButton(text="CLOSE",
                             on_release=lambda x: self.month_dialog.dismiss())
            ]
        )
        self.month_dialog.open()

    def _pick_month(self, month):
        self.selected_month = month
        self._update_month_label()
        if self.month_dialog:
            self.month_dialog.dismiss()
        self.calculate()

    # ── Year Picker ───────────────────────────
    def show_year_picker(self):
        current = datetime.datetime.now().year
        years = [str(y) for y in range(current - 2, current + 4)]
        items = [
            OneLineListItem(
                text=y,
                on_release=lambda x, yr=y: self._pick_year(yr)
            )
            for y in years
        ]
        self.year_dialog = MDDialog(
            title="Select Year",
            type="simple",
            items=items,
            buttons=[
                MDFlatButton(text="CLOSE",
                             on_release=lambda x: self.year_dialog.dismiss())
            ]
        )
        self.year_dialog.open()

    def _pick_year(self, year):
        self.selected_year = year
        self._update_month_label()
        if self.year_dialog:
            self.year_dialog.dismiss()
        self.calculate()

    # ── Core Calculation ──────────────────────
    def calculate(self, *args):
        ids = self.root.get_screen("root").ids

        def val(field_id):
            try:
                return float(ids[field_id].text or 0)
            except Exception:
                return 0.0

        mo = val("mo_field")
        work_hour = val("workhour_field")
        work_days = val("workdays_field")
        plan_sah = val("plan_sah_field")
        daily_earn = val("daily_earn_field")

        # Core formulas
        available_sah = work_hour * mo * work_days
        loading_sah = available_sah * 0.80
        earn_sah = daily_earn * work_days

        # Display main metrics
        ids.avail_label.text = f"{available_sah:,.1f}"
        ids.load_label.text = f"{loading_sah:,.1f}"
        ids.earn_label.text = f"{earn_sah:,.1f}"

        # ── Variation 1: Earn vs Available ────
        if available_sah > 0:
            var1 = earn_sah - available_sah
            pct1 = min(earn_sah / available_sah, 1.0)
            sign1 = "+" if var1 >= 0 else ""
            ids.var1_label.text = f"{sign1}{var1:,.1f}"
            if var1 >= 0:
                ids.var1_label.text_color = self._hex("#69F0AE")
                ids.var1_status.text = "✅ Earn exceeds Available"
                ids.var1_status.text_color = self._hex("#69F0AE")
                ids.var1_bar.md_bg_color = self._hex("#00E676")
            else:
                ids.var1_label.text_color = self._hex("#FF5252")
                ids.var1_status.text = "⚠️ Earn below Available"
                ids.var1_status.text_color = self._hex("#FF8A80")
                ids.var1_bar.md_bg_color = self._hex("#FF5252")
            anim = Animation(size_hint_x=max(pct1, 0.02), duration=0.5, t="out_quad")
            anim.start(ids.var1_bar)
        else:
            ids.var1_label.text = "—"
            ids.var1_status.text = "Enter factory inputs"
            Animation(size_hint_x=0.02, duration=0.3).start(ids.var1_bar)

        # ── Variation 2: Loading vs Earn ──────
        if loading_sah > 0 or earn_sah > 0:
            var2 = earn_sah - loading_sah
            base2 = max(loading_sah, earn_sah)
            pct2 = min(earn_sah / base2, 1.0) if base2 > 0 else 0
            sign2 = "+" if var2 >= 0 else ""
            ids.var2_label.text = f"{sign2}{var2:,.1f}"
            if var2 >= 0:
                ids.var2_label.text_color = self._hex("#69F0AE")
                ids.var2_status.text = "✅ Earn exceeds Loading"
                ids.var2_status.text_color = self._hex("#69F0AE")
                ids.var2_bar.md_bg_color = self._hex("#AB47BC")
            else:
                ids.var2_label.text_color = self._hex("#FF5252")
                ids.var2_status.text = "⚠️ Earn below Loading"
                ids.var2_status.text_color = self._hex("#FF8A80")
                ids.var2_bar.md_bg_color = self._hex("#7B1FA2")
            anim2 = Animation(size_hint_x=max(pct2, 0.02), duration=0.5, t="out_quad")
            anim2.start(ids.var2_bar)
        else:
            ids.var2_label.text = "—"
            ids.var2_status.text = "Enter factory inputs"
            Animation(size_hint_x=0.02, duration=0.3).start(ids.var2_bar)

        # ── Plan SAH vs Earn ──────────────────
        if plan_sah > 0 and earn_sah > 0:
            achieve_pct = (earn_sah / plan_sah) * 100
            diff = earn_sah - plan_sah
            sign = "+" if diff >= 0 else ""
            emoji = "🟢" if achieve_pct >= 100 else ("🟡" if achieve_pct >= 80 else "🔴")
            ids.plan_status_label.text = (
                f"{emoji}  {achieve_pct:.1f}% achieved  "
                f"({sign}{diff:,.1f} SAH vs Plan)"
            )
            if achieve_pct >= 100:
                ids.plan_status_label.text_color = self._hex("#69F0AE")
            elif achieve_pct >= 80:
                ids.plan_status_label.text_color = self._hex("#FFD740")
            else:
                ids.plan_status_label.text_color = self._hex("#FF5252")
        else:
            ids.plan_status_label.text = "— Enter Plan SAH & Daily Earn SAH"
            ids.plan_status_label.text_color = self._hex("#757575")

    def _hex(self, h):
        from kivy.utils import get_color_from_hex
        return get_color_from_hex(h)

    # ── Reset ─────────────────────────────────
    def reset_all(self):
        ids = self.root.get_screen("root").ids
        for fid in ["mo_field", "workhour_field", "workdays_field",
                    "plan_sah_field", "daily_earn_field"]:
            ids[fid].text = ""
        for lid in ["avail_label", "load_label", "earn_label",
                    "var1_label", "var2_label"]:
            ids[lid].text = "—"
        ids.var1_status.text = ""
        ids.var2_status.text = ""
        ids.plan_status_label.text = "—"
        for bar in ["var1_bar", "var2_bar"]:
            Animation(size_hint_x=0, duration=0.3).start(ids[bar])


if __name__ == "__main__":
    ApparelPlannerApp().run()
