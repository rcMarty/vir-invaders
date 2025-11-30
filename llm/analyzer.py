import json
import re
from typing import List

from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
from serde import SerdeError
from serde.json import to_json, from_json

from llm.dto import FileMetadata, BackupCandidate


def unwrap_code_block(response_text: str) -> str:
    if not response_text:
        return response_text

    stripped_text = response_text.strip()

    code_block_pattern = re.compile(
        r"^```(?:\w+)?\s*(.*?)\s*```$",
        re.DOTALL
    )

    match = code_block_pattern.match(stripped_text)
    if match:
        return match.group(1).strip()

    return stripped_text


class SensitiveFileScanner:

    def __init__(self, model: str, base_url: str, api_key: str = "") -> None:
        self.model_name: str = model
        self.client: OpenAI = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

    def analyze_files(self, file_list: List[FileMetadata]) -> List[BackupCandidate]:

        system_prompt: str = """
            You are a cybersecurity assistant. 
            Analyze a list of file metadata objects and identify which files must be backed up 
            because they contain or likely contain sensitive or legally important data.
            
            A file MUST be selected if ANY of the following apply:
            - Its preview contains personal data (full names with identifiers, SSN, ID numbers, 
              bank or card numbers, financial records, tax info, medical info, addresses, phone numbers).
            - Its preview contains credentials or secrets (passwords, API keys, tokens, OAuth secrets, 
              private keys, certificates, connection strings).
            - Its filename or extension commonly stores sensitive data, such as: .env, .yaml, .yml, .properties, 
              .conf, .cfg, .ini, .json, .xml, .pem, .p12, .pfx, .key, .keystore
            - Its path indicates configuration, secrets, credentials, ssl, certs, auth, keys, or similar names.
            - Its filename obviously implies sensitive content (contains words like: secret, token, 
              password, passwd, auth, cred, key, api, private, cert, tax, invoice, banking, statement, personal).
              
            Files should NOT be selected if:
            - They are images, videos, compiled binaries, caches, logs, or general documents that do NOT 
              contain sensitive data according to preview or naming.
            - Their preview shows no sensitive data and their names/paths do not imply sensitive content.
            
            Return a **single JSON object** with this structure:
            {
                "path": "Path to the file",
                "reason": "Brief explanation of why this file is a backup candidate",
                "risk_level": "HIGH" | "MEDIUM" | "LOW"
            }
        """

        user_prompt: str = f"""
            Analyze the following file metadata and return only the files that should be 
            considered backup candidates based on name, path, extension, or preview content:
            ```
            {to_json(file_list, indent=2)}
            ```
        """

        messages = [
            ChatCompletionSystemMessageParam(role="system", content=system_prompt),
            ChatCompletionUserMessageParam(role="user", content=user_prompt),
        ]

        response = self.client.chat.completions.create(
            model=self.model_name,
            temperature=0.2,
            messages=messages
        )

        response_content: str = response.choices[0].message.content
        response_content = unwrap_code_block(response_content)

        if not response_content:
            raise SerdeError("Empty model response")

        try:
            backup_candidates = []

            for item in json.loads(response_content):
                candidate = from_json(BackupCandidate, json.dumps(item))
                backup_candidates.append(candidate)

            return backup_candidates

        except json.JSONDecodeError as error:
            print("Invalid JSON returned:")
            print(response_content)
            raise SerdeError("Response was not valid JSON") from error

        except Exception as error:
            print("Unable to deserialize response:")
            print(response_content)
            raise SerdeError(error) from None


if __name__ == "__main__":
    scanner = SensitiveFileScanner(
        base_url="http://localhost:11434/v1",
        model="gemma3:4b"
    )

    files_to_analyze = [
        FileMetadata(
            path="/documents/tax_return_2023.pdf",
            name="tax_return_2023.pdf",
            extension=".pdf",
            size_kb=256,
            last_modified="2024-01-15T10:30:00Z",
            preview="""
                Name: John Doe
                SSN: 123-45-6789
                Income: $75,000
                Tax Paid: $15,000
                
                Bank Account: 987654321
                Routing Number: 021000021
            """
        ),
        FileMetadata(
            path="/pictures/vacation/photo1.jpg",
            name="photo1.jpg",
            extension=".jpg",
            size_kb=5120,
            last_modified="2023-12-20T14:00:00Z",
            preview=""
        ),
        FileMetadata(
            path="/home/user/projects/api-config.yaml",
            name="api-config.yaml",
            extension=".yaml",
            size_kb=3,
            last_modified="2025-10-02",
            preview="""
                api_key: "12345-ABCDE-67890-FGHIJ"
                database_url: "postgresql://user:password@localhost:5432/mydb"
            """
        ),
        FileMetadata(
            path="/notes/shopping_list.txt",
            name="shopping_list.txt",
            extension=".txt",
            size_kb=1,
            last_modified="2024-05-01T09:00:00Z",
            preview="""
                - Milk
                - Bread
                - Eggs
                - Butter
            """
        ),
    ]

    candidates = scanner.analyze_files(files_to_analyze)
    for candidate in candidates:
        print(f"Path: {candidate.path}")
        print(f"Reason: {candidate.reason}")
        print(f"Risk Level: {candidate.risk_level}")
        print("-----")
