import os
import pprint

from subprocess import Popen, PIPE
from typing import List, Optional, Dict

from src.common.logger_setup import logger


class Runner:
    @staticmethod
    def run(
        cmds: List[List[str]], env_vars: Optional[Dict[str, str]] = None
    ) -> Dict[str, str | int]:
        """
        run() can take multiple "sets" of commands and pass the stdout
        from one command to the stdin of the next. Hence, cmds is a List[List[str]]

        Eg,
        cmds = [
          ["cat", "foo.txt"],
          ["echo"],
        ]
        is equivalent to `cat foo.txt > echo`

        stderr is discarded as far as passing to the next stdin goes.

        Args:
            cmds (List[List[str]]): List of commands to run. stdout from previous commands are piped to the next command's stdin
            env_vars (Optional[Dict[str, str]], optional): Environment variables to set while running commands. Defaults to None

        Returns:
            Tuple[str, str, int]: Stdout, stdin, and returncode
        """

        env = os.environ.copy()
        if env_vars is not None:
            for key, value in env_vars.items():
                env[key] = value

        prev_stdout, prev_stderr = "", ""

        for cmd in cmds:
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE, env=env)
            logger.info(
                f"Starting Popen proc (pid:{proc.pid}) - Running {pprint.pformat(cmd)}"
            )
            stdout_b, stderr_b = proc.communicate(prev_stdout.encode("utf8"))

            prev_stdout, prev_stderr = stdout_b.decode("utf8"), stderr_b.decode("utf8")
            logger.info(f"Completed proc (pid:{proc.pid}) and got stdout/stderr")

            if prev_stdout:
                logger.info(prev_stdout)
            if prev_stderr:
                logger.warning(prev_stderr)

        return {
            "stdout": prev_stdout,
            "stderr": prev_stderr,
            "exit_code": proc.returncode,
        }
