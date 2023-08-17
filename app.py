import logging
import math
import time

import dash
import dash_chat_components as dch
from dash import Input, Output, State, html
from dash.exceptions import PreventUpdate
from chat_handler import process_chat_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = dash.Dash(__name__)

app = dash.Dash(
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"
    ]
)

messages = [
    {
      "direction": "received",
      "avatar": "bot.png",
      "content": "Hello!",
      "timestamp": int(math.floor(time.time() * 1000)),
    },
]


app.layout = html.Div([
    dch.Chat(
        [
            dch.ChatMessageList(
                [
                    dch.ChatMessage(
                        m["content"],
                        avatar=dash.get_asset_url(m["avatar"]),
                        direction=m["direction"],
                        timestamp=m["timestamp"]
                    ) for m in messages
                ],
                id="chat-msg-list",
                className="px-2",
                style={"height": "calc(100% - 65px)"}
            ),
            dch.ChatInput(
                id='chat-input',
                className="mt-2 mx-2",
                autofocus=True,
                style={"height": "65px"}
            ),
        ],
        className="h-100"
    ),
], style={
    'height': 'calc(100vh - 40px)',
    'margin': '20px auto',
    'max-width': '900px'
})


@app.callback(
    Output("chat-msg-list", "children", allow_duplicate=True),
    Output("chat-input", "disabled", allow_duplicate=True),
    Output("chat-input", "autofocus"),
    Input("chat-input", "n_submit"),
    State("chat-input", "n_submit_timestamp"),
    State("chat-input", "value_on_submit"),
    State("chat-msg-list", "children"), prevent_initial_call=True)
def send_message(n_submit, n_submit_timestamp, value_on_submit, msg_list):
    if n_submit is None:
        raise PreventUpdate
    else:
        msg_list.append(
            dch.ChatMessage(
                value_on_submit,
                avatar=dash.get_asset_url("user.png"),
                direction="outgoing",
                timestamp=n_submit_timestamp
            )
        )
        msg_list.append(
            dch.ChatMessageTyping(
                avatar="bot.png",
                direction="received",
            )
        )
    
        return msg_list, True, True


@app.callback(
    Output("chat-msg-list", "children"),
    Output("chat-input", "disabled"),
    Input("chat-msg-list", "children"),
    State("chat-input", "value_on_submit"),
    State("chat-msg-list", "children"), prevent_initial_call=True)
def reply_message(children, value_on_submit, msg_list):
    last_message = children[-2]["props"]
    if last_message["direction"] != "outgoing":
        raise PreventUpdate
    else:
        ai_response = process_chat_message(value_on_submit)
        msg_list.pop()
        msg_list.append(
            dch.ChatMessage(
                ai_response,
                avatar=dash.get_asset_url("bot.png"),
                direction="received",
                timestamp=int(math.floor(time.time() * 1000))
            )
        )
    
        return msg_list, False


if __name__ == '__main__':
    app.run_server(debug=True)
