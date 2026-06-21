import os

from dotenv import load_dotenv
load_dotenv()

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    # AgentServer,
    WorkerOptions,
    cli,
)

from livekit.plugins import (
    openai,
    assemblyai,
    deepgram,
    cartesia,
    silero,
    tavus,
    langchain
)

from livekit.plugins import (
    
    silero,
)

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from agent import agent

graph = agent

class Assistant(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a friendly healthcare voice assistant. "
                "Help patients book and manage appointments."
        )

# server = AgentServer()


# @server.rtc_session()
async def entrypoint(ctx: JobContext):
    await ctx.connect()

    session = AgentSession(
        vad=silero.VAD.load(),
        # stt=assemblyai.STT(
        #     # model="universal-streaming"
        # ),
        stt=deepgram.STT(model="nova-3", language="multi"),
        tts=cartesia.TTS(),
        llm=langchain.LLMAdapter(
            graph=graph
        )
    )

    avatar = tavus.AvatarSession(
        replica_id="r291e545fd67",
        # persona_id="pcb7a34da5fe",
        # Optional: avatar_participant_name="Healthcare Assistant"
    )

    await avatar.start(session, room=ctx.room)

    await session.start(
        room=ctx.room,
        agent=Assistant()
    )

    await session.generate_reply(
        instructions="Greet the user as a hospital front desk assistant."
    )


if __name__ == "__main__":
    print("URL:", os.getenv("LIVEKIT_URL"))
    print("KEY:", os.getenv("LIVEKIT_API_KEY"))
    print("SECRET:", os.getenv("LIVEKIT_API_SECRET"))
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint
        )
    )


# if __name__ == "__main__":
#     cli.run_app(server)