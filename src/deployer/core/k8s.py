import subprocess
import tempfile
import json
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class NATSDeployer:
    def __init__(self, kubeconfig_dict: Dict[str, Any]):
        self.kubeconfig_path = self._write_temp_kubeconfig(kubeconfig_dict)

    def _write_temp_kubeconfig(self, kubeconfig: Dict[str, Any]) -> str:
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            json.dump(kubeconfig, f)
            return f.name

    def deploy(self,
               release_name: str,
               helm_set_values: Dict[str, Any],
               namespace: str = "communication") -> bool:
        try:
            # Create namespace if it doesn't exist
            subprocess.run([
                "kubectl", "--kubeconfig", self.kubeconfig_path,
                "create", "namespace", namespace
            ], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            cmd = [
                "helm", "upgrade", "--install", release_name,
                "nats/nats",
                "--namespace", namespace,
                "--kubeconfig", self.kubeconfig_path,
                "-f", "/app/values.yaml"
            ]

            for key, value in helm_set_values.items():
                if isinstance(value, bool):
                    value = str(value).lower()
                cmd.extend(["--set", f"{key}={value}"])

            subprocess.run(cmd, check=True)
            logger.info(f"NATS deployed as '{release_name}' in namespace '{namespace}'")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Helm deployment failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False
        finally:
            self.cleanup()

    def uninstall(self, release_name: str, namespace: str = "communication") -> bool:
        
        try:
            cmd = [
                "helm", "uninstall", release_name,
                "--namespace", namespace,
                "--kubeconfig", self.kubeconfig_path
            ]
            subprocess.run(cmd, check=True)
            logger.info(f"NATS release '{release_name}' successfully uninstalled from namespace '{namespace}'")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to uninstall NATS release '{release_name}': {e}")
            return False
        finally:
            self.cleanup()

    def cleanup(self):
        if os.path.exists(self.kubeconfig_path):
            os.remove(self.kubeconfig_path)
    

    def upgrade(self,
                release_name: str,
                helm_set_values: Dict[str, Any],
                namespace: str = "communication") -> bool:
        try:
            cmd = [
                "helm", "upgrade", release_name,
                "nats/nats",
                "--namespace", namespace,
                "--kubeconfig", self.kubeconfig_path,
                "-f", "/app/values.yaml"
            ]

            for key, value in helm_set_values.items():
                if isinstance(value, bool):
                    value = str(value).lower()
                cmd.extend(["--set", f"{key}={value}"])

            subprocess.run(cmd, check=True)
            logger.info(f"NATS Helm release '{release_name}' upgraded in namespace '{namespace}'")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Helm upgrade failed: {e}")
            return False
        finally:
            self.cleanup()
