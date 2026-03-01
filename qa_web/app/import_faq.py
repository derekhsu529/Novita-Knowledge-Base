"""
FAQ 种子数据 - Novita AI
基于 novita-skills 知识库内容编写
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "qa.db"

FAQ_DATA = [
    # 一、Quick Start
    {
        "category": "Quick Start",
        "question": "How to get started with Novita AI?",
        "answer": "1. Sign up at https://novita.ai and get your API key from https://novita.ai/settings/key-management\n2. Install the OpenAI SDK: `pip install openai`\n3. Make your first API call:\n```python\nfrom openai import OpenAI\n\nclient = OpenAI(\n    base_url=\"https://api.novita.ai/openai/v1\",\n    api_key=\"your_api_key\"\n)\n\nresponse = client.chat.completions.create(\n    model=\"deepseek/deepseek-v3-0324\",\n    messages=[{\"role\": \"user\", \"content\": \"Hello!\"}]\n)\nprint(response.choices[0].message.content)\n```"
    },
    {
        "category": "Quick Start",
        "question": "What is the Novita AI API base URL?",
        "answer": "The Novita AI API base URL is:\n- **OpenAI compatible**: `https://api.novita.ai/openai/v1`\n\nAuthentication: Use `Authorization: Bearer <YOUR_API_KEY>` header."
    },
    {
        "category": "Quick Start",
        "question": "How to get an API key?",
        "answer": "Visit https://novita.ai/settings/key-management to create and manage your API keys. Keep your keys secure and never share them publicly."
    },
    # 二、LLM API
    {
        "category": "LLM API",
        "question": "What models does Novita AI support?",
        "answer": "Novita AI supports a wide range of models including:\n- **DeepSeek**: DeepSeek-V3, DeepSeek-R1\n- **Meta Llama**: Llama 3.1, Llama 3.3\n- **Qwen**: Qwen2.5, QwQ\n- **Google Gemini**: Gemini 2.0 Flash\n- **Mistral**: Mistral Large, Mistral Small\n\nCheck the full model catalog at https://novita.ai/models"
    },
    {
        "category": "LLM API",
        "question": "How to use tool calling / function calling?",
        "answer": "Novita AI supports OpenAI-compatible tool calling:\n```python\nresponse = client.chat.completions.create(\n    model=\"deepseek/deepseek-v3-0324\",\n    messages=[{\"role\": \"user\", \"content\": \"What's the weather?\"}],\n    tools=[{\n        \"type\": \"function\",\n        \"function\": {\n            \"name\": \"get_weather\",\n            \"description\": \"Get weather info\",\n            \"parameters\": {\n                \"type\": \"object\",\n                \"properties\": {\n                    \"location\": {\"type\": \"string\"}\n                },\n                \"required\": [\"location\"]\n            }\n        }\n    }]\n)\n```"
    },
    {
        "category": "LLM API",
        "question": "How to use JSON mode?",
        "answer": "Set `response_format={\"type\": \"json_object\"}` in your API call:\n```python\nresponse = client.chat.completions.create(\n    model=\"deepseek/deepseek-v3-0324\",\n    messages=[{\"role\": \"user\", \"content\": \"List 3 colors as JSON\"}],\n    response_format={\"type\": \"json_object\"}\n)\n```\nThe response will always be valid JSON."
    },
    {
        "category": "LLM API",
        "question": "How to use streaming?",
        "answer": "Use `stream=True` for streaming responses:\n```python\nstream = client.chat.completions.create(\n    model=\"deepseek/deepseek-v3-0324\",\n    messages=[{\"role\": \"user\", \"content\": \"Tell me a story\"}],\n    stream=True\n)\nfor chunk in stream:\n    if chunk.choices[0].delta.content:\n        print(chunk.choices[0].delta.content, end=\"\")\n```"
    },
    # 三、GPU Instances
    {
        "category": "GPU Instances",
        "question": "What GPU types are available?",
        "answer": "Novita AI offers:\n- **GPU Instance** (dedicated): Long-running workloads, full control\n  - NVIDIA A100, H100, L40S, RTX 4090, etc.\n- **Serverless GPU**: Pay-per-use, auto-scaling\n  - Ideal for inference workloads\n\nCheck pricing at https://novita.ai/pricing"
    },
    {
        "category": "GPU Instances",
        "question": "GPU Instance vs Serverless GPU - which to choose?",
        "answer": "**GPU Instance** (dedicated):\n- Best for: training, fine-tuning, persistent workloads\n- Full SSH access and root control\n- Billed per hour\n\n**Serverless GPU**:\n- Best for: inference, burst workloads\n- Auto-scaling, no infrastructure management\n- Pay per request/compute time\n\nChoose GPU Instance for consistent workloads, Serverless for variable demand."
    },
    # 四、Agent Sandbox
    {
        "category": "Agent Sandbox",
        "question": "What is Agent Sandbox?",
        "answer": "Agent Sandbox provides cloud-based isolated environments for AI agents to execute code, browse the web, and interact with files safely. Features:\n- SDK and CLI access\n- Pre-built templates\n- File upload/download\n- Lifecycle management (create, pause, resume, terminate)\n\nDocs: https://novita.ai/docs/guides/sandbox-overview"
    },
    {
        "category": "Agent Sandbox",
        "question": "How to create a sandbox?",
        "answer": "Use the Novita AI SDK:\n```python\nfrom novita_ai import NovitaClient\n\nclient = NovitaClient(api_key=\"your_key\")\nsandbox = client.sandbox.create(\n    template=\"python-3.11\",\n    name=\"my-sandbox\"\n)\nprint(sandbox.id)\n```\nOr use the REST API - see https://novita.ai/docs/guides/sandbox-overview for details."
    },
    # 五、Integrations
    {
        "category": "Integrations",
        "question": "How to use Novita AI with Cursor?",
        "answer": "1. Open Cursor Settings → Models\n2. Set API Base URL to `https://api.novita.ai/openai/v1`\n3. Enter your Novita AI API key\n4. Select a model (e.g., `deepseek/deepseek-v3-0324`)\n\nYou can now use Novita AI models directly in Cursor."
    },
    {
        "category": "Integrations",
        "question": "How to use Novita AI with LangChain?",
        "answer": "```python\nfrom langchain_openai import ChatOpenAI\n\nllm = ChatOpenAI(\n    base_url=\"https://api.novita.ai/openai/v1\",\n    api_key=\"your_novita_key\",\n    model=\"deepseek/deepseek-v3-0324\"\n)\n\nresponse = llm.invoke(\"Hello!\")\nprint(response.content)\n```"
    },
    {
        "category": "Integrations",
        "question": "How to use Novita AI with Continue (VS Code)?",
        "answer": "Add to your Continue config (`~/.continue/config.json`):\n```json\n{\n  \"models\": [{\n    \"title\": \"Novita AI\",\n    \"provider\": \"openai\",\n    \"model\": \"deepseek/deepseek-v3-0324\",\n    \"apiBase\": \"https://api.novita.ai/openai/v1\",\n    \"apiKey\": \"your_novita_key\"\n  }]\n}\n```"
    },
    # 六、Common Issues
    {
        "category": "Common Issues",
        "question": "API returns 401 Unauthorized?",
        "answer": "HTTP 401 means authentication failed. Check:\n1. API key is correct (no extra spaces)\n2. API key has not expired or been revoked\n3. Using the correct header: `Authorization: Bearer <API_KEY>`\n4. Account has sufficient balance\n\nRegenerate your API key at https://novita.ai/settings/key-management if needed."
    },
    {
        "category": "Common Issues",
        "question": "API returns 429 Too Many Requests?",
        "answer": "HTTP 429 means rate limit exceeded. Solutions:\n1. Reduce request frequency, add delays between calls\n2. Use exponential backoff retry strategy\n3. Check your current rate limits in the console\n4. Contact support on Discord for limit increases: https://discord.gg/YyPRAzwp7P"
    },
    {
        "category": "Common Issues",
        "question": "How to check pricing?",
        "answer": "Visit https://novita.ai/pricing for up-to-date pricing information.\n\nYou can also check model-specific pricing via API:\n```bash\ncurl https://api.novita.ai/openai/v1/models \\\n  -H \"Authorization: Bearer $NOVITA_API_KEY\"\n```"
    },
    {
        "category": "Common Issues",
        "question": "How to contact support?",
        "answer": "You can reach Novita AI support through:\n- **Discord**: https://discord.gg/YyPRAzwp7P\n- **Documentation**: https://novita.ai/docs\n- **Console**: https://novita.ai/console"
    },
]


def import_faq():
    """导入FAQ数据到手工知识库"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH))

    conn.execute("""
        CREATE TABLE IF NOT EXISTS manual_kb (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_manual_kb_category ON manual_kb(category)")

    cursor = conn.execute("SELECT COUNT(*) FROM manual_kb")
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"手工知识库已有 {count} 条数据。")
        choice = input("是否清空后重新导入？(y/N): ").strip().lower()
        if choice == 'y':
            conn.execute("DELETE FROM manual_kb")
            print("已清空旧数据。")
        else:
            print("取消导入。")
            conn.close()
            return

    for faq in FAQ_DATA:
        conn.execute(
            "INSERT INTO manual_kb (category, question, answer) VALUES (?, ?, ?)",
            (faq["category"], faq["question"], faq["answer"])
        )

    conn.commit()

    cursor = conn.execute("SELECT category, COUNT(*) FROM manual_kb GROUP BY category ORDER BY category")
    print(f"\n导入完成！共 {len(FAQ_DATA)} 条FAQ：")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} 条")

    conn.close()


if __name__ == "__main__":
    import_faq()
