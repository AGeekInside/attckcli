import json

import click
from textual.app import App
from textual import events
from textual.widgets import Placeholder, Header, Footer, ScrollView, TreeControl, TreeClick, NodeID

ATTCK_DICT = {}


def process_attck(attck_dict):
    attck_info = {
        
    }


class ATTCKApp(App):
    async def on_load(self) -> None:

        # Bind keys
        await self.bind("b", "view.toggle('technique_tree')", "Toggle Technique Tree")
        await self.bind("q", "quit", "Quit")

        self.processed_attck = process_attck(ATTCK_DICT)

    async def on_mount(self, event: events.Mount) -> None:

        self.body = ScrollView()
        self.listing = Placeholder()

        # Dock our widgets
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")

        technique_tree = TreeControl("Technique Tree", data="root")
        # for node_num in range(4):
            # technique_tree.add(node_id=NodeID(node_num),label=f"node_{node_num}")

        await self.view.dock(technique_tree, name="technique_tree")
        # await self.view.dock(ScrollView(self.listing), edge="left", size=48, name="sidebar") 
        await self.view.dock(self.body, edge="top")

        async def handle_tree_click(self, message: TreeClick) -> None:
            if message.node.empty:
                await message.node.add("foo")
                await message.node.add("bar")
                await message.node.add("baz")
                await message.node.expand()
            else:
                await message.node.toggle()


@click.command
@click.argument("attck_json", envvar="ATTCK_JSON")
def tui(attck_json):
    with open(attck_json) as input_json:
        ATTCK_DICT = json.load(input_json)

    # print(ATTCK_DICT) 
    ATTCKApp.run(title="ATT&CK Viewer App", log="textual.log")