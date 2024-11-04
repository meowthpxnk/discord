from typing import Optional, Union

from app import db, id_encryptor, logger
from app.api.routes.__auth_dependencies import (
    CurrentUser,
    UserTokenDataDepends,
    auth_failed_responses,
)
from app.api.routes._base_router import APIRouter
from app.database.errors import AlreadyExistsInDB, NotFoundInDB
from app.database.models import Chat, Message, Server, ServerUser, VoiceChat
from app.database.models.Chat import ChatForm
from app.database.models.Message import MessageForm
from app.database.models.Server import ServerForm
from app.database.models.ServerUser import ServerUserForm, ServerUserRoleEnum
from app.database.models.VoiceChat import VoiceChatForm
from app.schemas import (
    ChatResponseModel,
    MessageRequestForm,
    MessageResponseModel,
    ServerRequestForm,
    ServerResponseModel,
)


router = APIRouter(
    tags=["Server"],
    dependencies=[UserTokenDataDepends],
    responses=auth_failed_responses,
    prefix="/server",
)


@router.post("")
def create_server(form: ServerRequestForm, user: CurrentUser) -> None:
    logger.info(f"Creating server with title {form.title}")
    logger.debug(f"Creating server form {form}")

    try:
        Server.exists(Server.title == form.title)
    except AlreadyExistsInDB:
        raise Exception(f"Already existed server with title {form.title}")

    server = Server(ServerForm(title=form.title))

    db.session.add(server)

    server_user = ServerUser(
        ServerUserForm(user_id=user.id, role=ServerUserRoleEnum.OWNER)
    )
    server.users.append(server_user)

    chat = Chat(ChatForm(title="general"))
    server.chats.append(chat)

    voice_chat = VoiceChat(VoiceChatForm(title="general"))
    server.voice_chats.append(voice_chat)

    db.session.commit()


@router.get("")
def get_servers(
    user: CurrentUser, server_id: Optional[str] = None
) -> Union[list[ServerResponseModel], ServerResponseModel]:
    logger.info(f"Get user {user.username} servers")

    if not server_id:
        return [server_user.server.jsonify() for server_user in user.servers]

    try:
        server_id = id_encryptor.decrypt_id(server_id)
    except:
        raise Exception("Not valid server id")

    try:
        server_user = ServerUser.select_where(
            ServerUser.user_id == user.id,
            ServerUser.server_id == server_id,
            first=True,
        )
    except NotFoundInDB:
        raise Exception("Not valid server id")

    return server_user.server.jsonify()


@router.get("/chat")
def get_server_chats(
    user: CurrentUser, server_id: str, chat_id: Optional[str] = None
) -> Union[list[ChatResponseModel], ChatResponseModel]:
    logger.info(f"Get user {user.username} servers")

    try:
        server_id = id_encryptor.decrypt_id(server_id)
    except:
        raise Exception("Not valid server id")

    try:
        server_user = ServerUser.select_where(
            ServerUser.user_id == user.id,
            ServerUser.server_id == server_id,
            first=True,
        )
    except NotFoundInDB:
        raise Exception("Not valid server id")

    if not chat_id:
        return [chat.jsonify() for chat in server_user.server.chats]

    try:
        chat_id = id_encryptor.decrypt_id(chat_id)
    except:
        raise Exception("Not valid chat id")

    try:
        chat = Chat.select_where(Chat.id == chat_id, first=True)

    except NotFoundInDB:
        raise Exception("Not valid chat id")

    if not chat.server.id == server_user.server_id:
        raise Exception("Not valid chat id")

    return chat.jsonify()


@router.get("/chat/message")
def get_server_chat_messages(
    user: CurrentUser, chat_id: str
) -> list[MessageResponseModel]:
    logger.info(f"Get user {user.username} servers")

    try:
        chat_id = id_encryptor.decrypt_id(chat_id)
    except:
        raise Exception("Not valid chat id")

    try:
        chat = Chat.select_where(Chat.id == chat_id, first=True)
    except NotFoundInDB:
        raise Exception("Not valid chat id")

    try:
        ServerUser.select_where(
            ServerUser.user_id == user.id,
            ServerUser.server_id == chat.server.id,
            first=True,
        )
    except NotFoundInDB:
        raise Exception("Not valid chat id")

    return [message.jsonify() for message in chat.messages]


@router.post("/chat/message")
def post_message_to_chat(
    user: CurrentUser, chat_id: str, form: MessageRequestForm
) -> None:
    logger.info(f"Get user {user.username} servers")

    try:
        chat_id = id_encryptor.decrypt_id(chat_id)
    except:
        raise Exception("Not valid chat id")

    try:
        chat = Chat.select_where(Chat.id == chat_id, first=True)
    except NotFoundInDB:
        raise Exception("Not valid chat id")

    try:
        ServerUser.select_where(
            ServerUser.user_id == user.id,
            ServerUser.server_id == chat.server.id,
            first=True,
        )
    except NotFoundInDB:
        raise Exception("Not valid chat id")

    message = Message(MessageForm(body=form.body, user_id=user.id))
    chat.messages.append(message)
    db.session.commit()
