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

        # ==================================================
        # CORE SERVICES
        # ==================================================

        self.container = ServiceContainer()

        self.config = ConfigManager()

        self.service_manager = ServiceManager(
            self.config
        )

        self.logger_service = LoggerService()

        # ==================================================
        # SCOOBA COMPONENTS
        # ==================================================

        self.voice = VoiceManager()

        self.brain = Brain()

        self.ai = AIEngine()

        self.skills = SkillManager()

        self.dispatcher = AIDispatcher()

        self.planner = Planner()

        # IMPORTANT:
        #
        # Executor uses the SAME SkillManager
        # instance as SCOOBA.
        #
        self.executor = Executor(
            self.skills
        )

        # ==================================================
        # STATE
        # ==================================================

        self.state = AssistantState.BOOTING

        # ==================================================
        # REGISTER SERVICES
        # ==================================================

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

        # ==================================================
        # CONFIGURATION
        # ==================================================

        self.name = self.config.get(
            "assistant.name"
        )

        self.version = self.config.get(
            "assistant.version"
        )

    # ==================================================
    # STATE
    # ==================================================

    def set_state(
        self,
        state: AssistantState
    ):

        self.state = state

        logger.info(
            f"SCOOBA State -> {state.value}"
        )

    # ==================================================
    # START
    # ==================================================

    def start(self):

        # ==================================================
        # BOOT
        # ==================================================

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

        # ==================================================
        # GREETING
        # ==================================================

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

        # ==================================================
        # MICROPHONES
        # ==================================================

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

        # ==================================================
        # MAIN LOOP
        # ==================================================

        try:

            while True:

                # ------------------------------------------
                # LISTENING
                # ------------------------------------------

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

                # ------------------------------------------
                # AI
                # ------------------------------------------

                decision = self.ai.think(
                    text
                )

                # ------------------------------------------
                # EXIT DETECTION
                # ------------------------------------------

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
                    or
                    decision.intent
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

                # ------------------------------------------
                # PLANNING
                # ------------------------------------------

                plan = (
                    self.planner.create_plan(
                        decision
                    )
                )

                # ------------------------------------------
                # EXECUTION
                # ------------------------------------------
                #
                # Executor receives the complete plan.
                #
                # IMPORTANT:
                #
                # Do NOT additionally call:
                #
                # self.skills.execute(decision)
                #
                # Otherwise commands can execute twice.
                #

                success = (
                    self.executor.execute(
                        plan
                    )
                )

                # ------------------------------------------
                # RESULT
                # ------------------------------------------

                print(
                    f"\n📊 Execution Result: "
                    f"{'SUCCESS' if success else 'FAILED'}"
                )

                # ------------------------------------------
                # PERSONALITY RESPONSE
                # ------------------------------------------

                response = (
                    self.dispatcher.response(
                        decision,
                        success
                    )
                )

                # ------------------------------------------
                # SPEAK RESPONSE
                # ------------------------------------------

                if response:

                    self.set_state(
                        AssistantState.SPEAKING
                    )

                    self.voice.tts.speak(
                        response
                    )

                    self.set_state(
                        AssistantState.READY
                    )

        # ==================================================
        # KEYBOARD INTERRUPT
        # ==================================================

        except KeyboardInterrupt:

            print(
                "\n\n👋 SCOOBA interrupted."
            )

            logger.info(
                "SCOOBA interrupted by user."
            )

            self.set_state(
                AssistantState.READY
            )