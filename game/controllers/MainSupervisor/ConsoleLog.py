import AutoInstall
AutoInstall._import("cl", "termcolor")

class Console:
    PREFIX_ERROR: str = "[EREBUS ERROR]"
    PREFIX_WARN: str = "[EREBUS WARNING]"
    PREFIX_SUCC: str = "[EREBUS]"
    PREFIX_INFO: str = "[EREBUS INFO]"

    COLOR_ERROR: str = "red"
    COLOR_WARN: str = "orange"
    COLOR_SUCC: str = "green"
    COLOR_INFO: str = "blue"

    @staticmethod
    def log_err(msg: str) -> None:
        print(cl.colored(f"{Console.PREFIX_ERROR} {msg}", Console.COLOR_ERROR))
    
    @staticmethod
    def log_succ(msg: str) -> None:
        print(cl.colored(f"{Console.PREFIX_SUCC} {msg}", Console.COLOR_SUCC))

    @staticmethod
    def log_warn(msg: str) -> None:
        print(cl.colored(f"{Console.PREFIX_WARN} {msg}", Console.COLOR_WARN))

    @staticmethod
    def log_info(msg: str) -> None:
        print(cl.colored(f"{Console.PREFIX_INFO} {msg}", Console.COLOR_INFO))
