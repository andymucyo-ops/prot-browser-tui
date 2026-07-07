

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Vertical
from textual.widgets import DataTable, Footer, Header, Input, Static

from prot_browser_tui import UNIPROT_API_URL, extract_display_data, get_search_results
from .helpers import _data_as_ROWS


class BrowserApp(App):
    """
    main sreen displaying Title, search bar and search options. 
    """
    BINDINGS: list[BindingType] = [
            Binding("ctrl+q", "quit", "Quit"),
            ]
    CSS_PATH = "ui.tcss"
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="browser"):
                yield Static("Protein Brower", classes="title")
                yield Input(placeholder="Protein name", type="text", classes="input")
        yield Static(id="status")
        yield DataTable(id="results")
        yield Footer()

    @on(Input.Submitted)
    async def render_results(self, event: Input.Submitted) -> str:
        prot_name = event.value
        results = await get_search_results(UNIPROT_API_URL, prot_name) 
        display_data = extract_display_data(results)
        if isinstance(display_data, str):
            status = self.query_one("#status", Static)
            status.display = True
            status.update(display_data)
        else:
            ROWS: list[tuple[int, str, str, str]] = _data_as_ROWS(display_data)
            table = self.query_one(DataTable)
            table.clear(columns=True)
            table.display = True
            table.cursor_type = "row"
            table.add_columns(*ROWS[0])
            table.add_rows(ROWS[1:])



if __name__ == "__main__":
    app = BrowserApp()
    app.run()
