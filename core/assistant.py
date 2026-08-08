"""
==================================================
SCOOBA

Main Assistant Controller

Author: Sachin
==================================================
"""

from config.settings import ConfigManager
from core.container import ServiceContainer
from core.state import AssistantState

from services.logger_service import LoggerService
from services.service_manager import ServiceManager

from utils.logger import logger

from voice.manager import VoiceManager

from brain import Brain

from ai.engine import AIEngine
from skills.manager import SkillManager
from ai.dispatcher import AIDispatcher

from planner.planner import Planner
from planner.executor import Executor


class SCOOBA:

    def __init__(self):

        self.container = ServiceContainer()

        self.config = ConfigManager()

        self.service_manager = ServiceManager(
            self.config
        )

        self.logger_service = LoggerService()

        self.voice = VoiceManager()

        self.brain = Brain()

        self.ai = AIEngine()

        self.skills = SkillManager()

        self.dispatcher = AIDispatcher()

        self.planner = Planner()

        self.executor = Executor()

        self.state = AssistantState.BOOTING

        # ---------------------------------
        # Register Services
        # ---------------------------------

        self.service_manager.register(
            "Logger Service",
            self.logger_service
        )

        self.container.register(
            "config",
            self.config
        )

        self.container.register(
            "logger",
            logger
        )

        self.container.register(
            "service_manager",
            self.service_manager
        )

        self.container.register(
            "voice",
            self.voice
        )

        self.container.register(
            "brain",
            self.brain
        )

        self.container.register(
            "ai",
            self.ai
        )

        self.container.register(
            "skills",
            self.skills
        )

        self.container.register(
            "planner",
            self.planner
        )

        self.container.register(
            "executor",
            self.executor
        )

        # ---------------------------------
        # Configuration
        # ---------------------------------

        self.name = self.config.get(
            "assistant.name"
        )

        self.version = self.config.get(
            "assistant.version"
        )

    def set_state(
        self,
        state: AssistantState
    ):

        self.state = state

        logger.info(
            f"SCOOBA State -> {state.value}"
        )

    def start(self):

        # ---------------------------------
        # BOOT
        # ---------------------------------

        self.set_state(
            AssistantState.BOOTING
        )

        logger.info(
            "SCOOBA boot sequence started."
        )

        self.service_manager.start_all()

        print("=" * 50)

        print(
            f"{self.name} v{self.version}"
        )

        print("=" * 50)

        # ---------------------------------
        # GREETING
        # ---------------------------------

        self.set_state(
            AssistantState.SPEAKING
        )

        self.voice.greet()

        self.set_state(
            AssistantState.READY
        )

        print(
            f"\n🟢 Current State : "
            f"{self.state.value}"
        )

        # ---------------------------------
        # MICROPHONES
        # ---------------------------------

        print(
            "\n🎤 Available Microphones\n"
        )

        microphones = (
            self.voice.list_microphones()
        )

        for i, mic in enumerate(
            microphones,
            start=1
        ):

            print(
                f"[{i}] {mic['name']}"
            )

        print(
            "\n🚀 SCOOBA is ready."
        )

        print(
            "Say 'exit' to stop.\n"
        )

        # ---------------------------------
        # MAIN LOOP
        # ---------------------------------

        try:

            while True:

                self.set_state(
                    AssistantState.LISTENING
                )

                text = self.voice.listen()

                self.set_state(
                    AssistantState.READY
                )

                if not text:

                    continue

                print(
                    f"\n📝 Recognized : {text}"
                )

                # ---------------------------------
                # AI Decision
                # ---------------------------------

                decision = self.ai.think(
                    text
                )

                # ---------------------------------
                # EXIT DETECTION
                # ---------------------------------

                normalized_text = (
                    text
                    .lower()
                    .strip()
                    .rstrip(
                        "!.,?;:"
                    )
                )

                exit_commands = [
                    "exit",
                    "quit",
                    "stop",
                    "goodbye"
                ]

                if (
                    normalized_text
                    in exit_commands
                    or decision.intent
                    == "CLOSE_APP"
                ):

                    self.set_state(
                        AssistantState.SPEAKING
                    )

                    self.voice.tts.speak(
                        "Goodbye, CTO."
                    )

                    print(
                        "\n👋 SCOOBA "
                        "shutting down."
                    )

                    logger.info(
                        "SCOOBA stopped."
                    )

                    self.set_state(
                        AssistantState.READY
                    )

                    break

                # ---------------------------------
                # Planning
                # ---------------------------------

                plan = (
                    self.planner.create_plan(
                        decision
                    )
                )

                # ---------------------------------
                # Execute Plan
                # ---------------------------------

                self.executor.execute(
                    plan
                )

                # ---------------------------------
                # Execute Skill
                # ---------------------------------

                success = (
                    self.skills.execute(
                        decision
                    )
                )

                # ---------------------------------
                # Personality Response
                # ---------------------------------

                response = (
                    self.dispatcher.response(
                        decision
                    )
                )

                self.set_state(
                    AssistantState.SPEAKING
                )

                self.voice.tts.speak(
                    response
                )

                self.set_state(
                    AssistantState.READY
                )

        except KeyboardInterrupt:

            print(
                "\n\n👋 SCOOBA interrupted."
            )

            logger.info(
                "SCOOBA interrupted by user."
            )