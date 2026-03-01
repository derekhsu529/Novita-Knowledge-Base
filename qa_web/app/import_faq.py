"""
FAQ 种子数据 - Novita AI
来源: FAQ-Novita.pdf (38条)
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "qa.db"

FAQ_DATA = [
    # 一、Account & Registration (Q1-Q5)
    {
        "category": "Account",
        "question": "How do I create a Novita AI account?",
        "answer": "Visit novita.ai, click Sign Up, and register with your email. You'll receive free credits to explore AI models upon registration."
    },
    {
        "category": "Account",
        "question": "Do I get free credits after signing up?",
        "answer": "Yes. New users receive complimentary trial credits to access various AI model APIs including DeepSeek, Llama, Qwen, Gemini, and more. Check novita.ai for the exact amount."
    },
    {
        "category": "Account",
        "question": "How do I get my API key?",
        "answer": "Log in to Novita AI, navigate to Settings > Key Management (novita.ai/settings/key-management), and click Create New Key. Keep your API key secure."
    },
    {
        "category": "Account",
        "question": "What if I forget my password?",
        "answer": "Click Forgot Password on the login page and follow the email verification process to reset your password."
    },
    {
        "category": "Account",
        "question": "Can I have multiple API keys?",
        "answer": "Yes. You can create multiple API keys for different projects or environments from the Key Management page. Each key can be independently revoked."
    },
    # 二、Billing & Pricing (Q6-Q10)
    {
        "category": "Billing",
        "question": "How do I add funds?",
        "answer": "Log in and go to the Billing page. Novita AI supports credit card and other payment methods. Funds are available immediately."
    },
    {
        "category": "Billing",
        "question": "How does billing work?",
        "answer": "Billing is token-based (pay-as-you-go). Different models have different per-token prices. Check novita.ai/pricing for input/output rates per model."
    },
    {
        "category": "Billing",
        "question": "Can I get a refund?",
        "answer": "Refunds are generally not available after payment. We recommend using the free credits first. For special circumstances, contact support via Discord."
    },
    {
        "category": "Billing",
        "question": "How do I check my usage?",
        "answer": "Log in to the Console (novita.ai/console) to see detailed API call records including model, token count, and cost per request."
    },
    {
        "category": "Billing",
        "question": "Are there volume discounts?",
        "answer": "For high-volume usage, contact our sales team through Discord (discord.gg/YyPRAzwp7P) to discuss custom pricing plans."
    },
    # 三、API Usage (Q11-Q16)
    {
        "category": "API",
        "question": "What is the Novita AI API base URL?",
        "answer": "The API base URL is:\n- OpenAI-compatible: `https://api.novita.ai/openai/v1`\n\nSet this as the `base_url` in your SDK."
    },
    {
        "category": "API",
        "question": "What AI models are supported?",
        "answer": "Novita AI supports 100+ models including:\n- **DeepSeek**: V3, R1\n- **Meta Llama**: 3.1, 3.3\n- **Qwen**: 2.5, QwQ-32B\n- **Google Gemini**: 2.0 Flash\n- **Mistral**: Large, Small\n- **Image**: FLUX, Stable Diffusion\n\nFull list at novita.ai/models."
    },
    {
        "category": "API",
        "question": "How do I call the API with OpenAI SDK?",
        "answer": "Simply change base_url and api_key:\n\n```python\nfrom openai import OpenAI\n\nclient = OpenAI(\n    base_url=\"https://api.novita.ai/openai/v1\",\n    api_key=\"your_novita_api_key\"\n)\n\nresponse = client.chat.completions.create(\n    model=\"deepseek/deepseek-v3-0324\",\n    messages=[{\"role\": \"user\", \"content\": \"Hello\"}]\n)\nprint(response.choices[0].message.content)\n```"
    },
    {
        "category": "API",
        "question": "How do I use streaming?",
        "answer": "Use `stream=True`:\n\n```python\nstream = client.chat.completions.create(\n    model=\"deepseek/deepseek-v3-0324\",\n    messages=[{\"role\": \"user\", \"content\": \"Tell me a story\"}],\n    stream=True\n)\nfor chunk in stream:\n    if chunk.choices[0].delta.content:\n        print(chunk.choices[0].delta.content, end=\"\")\n```"
    },
    {
        "category": "API",
        "question": "API returns 401 - what should I do?",
        "answer": "HTTP 401 means authentication failed. Check:\n1. API Key is correct (no extra spaces)\n2. API Key is not expired or revoked\n3. Account has sufficient balance\n4. base_url is correctly configured\n\nTry regenerating a new API Key if the issue persists."
    },
    {
        "category": "API",
        "question": "API returns 429 - what should I do?",
        "answer": "HTTP 429 means rate limit exceeded. Solutions:\n1. Reduce request frequency with delays\n2. Use exponential backoff retry\n3. Contact support on Discord for higher limits: discord.gg/YyPRAzwp7P"
    },
    # 四、Models (Q17-Q22)
    {
        "category": "Models",
        "question": "What are the differences between models?",
        "answer": "Key model characteristics:\n- **DeepSeek-V3/R1**: Strong reasoning and coding\n- **Llama 3.3**: Good general-purpose, open source\n- **Qwen2.5**: Strong multilingual support\n- **Gemini 2.0 Flash**: Fast, vision + long context (1M tokens)\n- **Mistral Large**: Strong European languages\n\nChoose based on your use case. Details at novita.ai/models."
    },
    {
        "category": "Models",
        "question": "What are the context length limits?",
        "answer": "Context lengths vary by model:\n- DeepSeek-V3: 128K tokens\n- Llama 3.3: 128K tokens\n- Qwen2.5: 128K tokens\n- Gemini 2.0 Flash: 1M tokens\n- Mistral Large: 128K tokens\n\nLonger context = higher cost per call."
    },
    {
        "category": "Models",
        "question": "Which models support vision/multimodal input?",
        "answer": "Models with vision support:\n- Google Gemini 2.0 Flash\n- Other vision models as listed at novita.ai/models\n\nPass images as base64 data or URLs in the messages parameter."
    },
    {
        "category": "Models",
        "question": "How do I use tool calling / function calling?",
        "answer": "Novita AI supports OpenAI-compatible tool calling:\n```python\nresponse = client.chat.completions.create(\n    model=\"deepseek/deepseek-v3-0324\",\n    messages=[{\"role\": \"user\", \"content\": \"What's the weather?\"}],\n    tools=[{\n        \"type\": \"function\",\n        \"function\": {\n            \"name\": \"get_weather\",\n            \"parameters\": {\"type\": \"object\", \"properties\": {\"location\": {\"type\": \"string\"}}}\n        }\n    }]\n)\n```"
    },
    {
        "category": "Models",
        "question": "How do I use JSON mode?",
        "answer": "Set `response_format={\"type\": \"json_object\"}`:\n```python\nresponse = client.chat.completions.create(\n    model=\"deepseek/deepseek-v3-0324\",\n    messages=[{\"role\": \"user\", \"content\": \"List 3 colors as JSON\"}],\n    response_format={\"type\": \"json_object\"}\n)\n```"
    },
    {
        "category": "Models",
        "question": "How do I get the latest model list?",
        "answer": "Fetch live model data via API:\n```bash\ncurl https://api.novita.ai/openai/v1/models \\\n  -H \"Authorization: Bearer $NOVITA_API_KEY\"\n```\nOr visit novita.ai/models for the web catalog."
    },
    # 五、Integration (Q23-Q28)
    {
        "category": "Integration",
        "question": "How do I use Novita AI in Cursor?",
        "answer": "1. Open Cursor Settings → Models\n2. Set API Base URL to `https://api.novita.ai/openai/v1`\n3. Enter your Novita AI API Key\n4. Select a model (e.g., `deepseek/deepseek-v3-0324`)"
    },
    {
        "category": "Integration",
        "question": "How do I use Novita AI in Continue (VS Code)?",
        "answer": "Add to `~/.continue/config.json`:\n```json\n{\n  \"models\": [{\n    \"title\": \"Novita AI\",\n    \"provider\": \"openai\",\n    \"model\": \"deepseek/deepseek-v3-0324\",\n    \"apiBase\": \"https://api.novita.ai/openai/v1\",\n    \"apiKey\": \"your_key\"\n  }]\n}\n```"
    },
    {
        "category": "Integration",
        "question": "How do I use Novita AI with LangChain?",
        "answer": "```python\nfrom langchain_openai import ChatOpenAI\n\nllm = ChatOpenAI(\n    base_url=\"https://api.novita.ai/openai/v1\",\n    api_key=\"your_key\",\n    model=\"deepseek/deepseek-v3-0324\"\n)\nresponse = llm.invoke(\"Hello!\")\n```"
    },
    {
        "category": "Integration",
        "question": "How do I use Novita AI with LlamaIndex?",
        "answer": "```python\nfrom llama_index.llms.openai_like import OpenAILike\n\nllm = OpenAILike(\n    api_base=\"https://api.novita.ai/openai/v1\",\n    api_key=\"your_key\",\n    model=\"deepseek/deepseek-v3-0324\"\n)\nresponse = llm.complete(\"Hello!\")\n```"
    },
    {
        "category": "Integration",
        "question": "How do I set up observability with Langfuse?",
        "answer": "Novita AI works with Langfuse for monitoring:\n1. Set up a Langfuse account\n2. Use Langfuse's SDK wrapper around your Novita AI calls\n3. Monitor latency, token usage, and costs in the Langfuse dashboard"
    },
    {
        "category": "Integration",
        "question": "What other tools are supported?",
        "answer": "Most OpenAI-compatible tools work with Novita AI. Common integrations:\n- **IDE**: Cursor, Continue, Cline\n- **Frameworks**: LangChain, LlamaIndex\n- **Chat UI**: ChatBox, NextChat, LobeChat, Open WebUI\n- **Observability**: Langfuse, Helicone\n\nGeneral setup: set Base URL to `https://api.novita.ai/openai/v1` and enter your API key."
    },
    # 六、GPU (Q29-Q32)
    {
        "category": "GPU",
        "question": "What GPU types are available?",
        "answer": "Novita AI offers:\n- **GPU Instance** (dedicated): NVIDIA A100, H100, L40S, RTX 4090\n- **Serverless GPU**: Pay-per-use, auto-scaling\n\nPricing at novita.ai/pricing."
    },
    {
        "category": "GPU",
        "question": "GPU Instance vs Serverless GPU?",
        "answer": "**GPU Instance**: Best for training, fine-tuning, persistent workloads. Full SSH access, billed per hour.\n\n**Serverless GPU**: Best for inference, burst workloads. Auto-scaling, pay per compute time.\n\nChoose Instance for consistent loads, Serverless for variable demand."
    },
    {
        "category": "GPU",
        "question": "How do I launch a GPU Instance?",
        "answer": "1. Log in to novita.ai/console\n2. Go to GPU Instances\n3. Select GPU type (A100, H100, etc.)\n4. Choose a template or custom Docker image\n5. Configure storage and networking\n6. Launch\n\nDocs: novita.ai/docs/guides/gpu-instance-overview"
    },
    {
        "category": "GPU",
        "question": "What are the GPU pricing tiers?",
        "answer": "GPU pricing varies by type and commitment:\n- On-demand: Pay per hour\n- Reserved: Discounted rates for longer commitments\n\nCheck novita.ai/pricing for current rates. Contact sales on Discord for custom plans."
    },
    # 七、Sandbox (Q33-Q35)
    {
        "category": "Sandbox",
        "question": "What is Agent Sandbox?",
        "answer": "Cloud-based isolated environments for AI agents to safely execute code, browse the web, and manage files. Features:\n- SDK and CLI access\n- Pre-built templates (Python, Node.js)\n- File upload/download\n- Lifecycle management\n\nDocs: novita.ai/docs/guides/sandbox-overview"
    },
    {
        "category": "Sandbox",
        "question": "How do I create a sandbox?",
        "answer": "Via REST API:\n```bash\ncurl -X POST https://api.novita.ai/v1/sandboxes \\\n  -H \"Authorization: Bearer YOUR_API_KEY\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"template\": \"python-3.11\", \"name\": \"my-sandbox\"}'\n```\n\nSee novita.ai/docs/guides/sandbox-overview for SDK usage."
    },
    {
        "category": "Sandbox",
        "question": "What templates are available?",
        "answer": "Pre-built templates include:\n- Python 3.11\n- Node.js\n- Custom Docker images\n\nTemplates come with common tools pre-installed. Check the docs for the latest list."
    },
    # 八、Support (Q36-Q38)
    {
        "category": "Support",
        "question": "How do I contact support?",
        "answer": "Reach Novita AI support:\n- **Discord**: discord.gg/YyPRAzwp7P\n- **Docs**: novita.ai/docs\n- **Console**: novita.ai/console"
    },
    {
        "category": "Support",
        "question": "Is there technical documentation?",
        "answer": "Yes. Full docs at novita.ai/docs including:\n- Quick start guide\n- API reference\n- Model details\n- Code examples (Python, JavaScript, cURL)\n- FAQ & troubleshooting"
    },
    {
        "category": "Support",
        "question": "API is slow - what can I do?",
        "answer": "If responses are slow:\n1. Use a faster/smaller model\n2. Reduce max_tokens\n3. Shorten input length\n4. Use streaming (stream=true)\n5. Check network connectivity\n\nReport persistent issues on Discord."
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
