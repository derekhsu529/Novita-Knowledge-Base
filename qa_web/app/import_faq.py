"""
FAQ 种子数据 - Novita AI
基于 novita-skills 知识库内容编写
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "qa.db"

FAQ_DATA = [
    # 一、账户与注册
    {
        "category": "账户与注册",
        "question": "如何注册接口AI账户？",
        "answer": "访问 jiekou.ai 官网，点击「注册/登录」按钮，可以使用手机号注册。注册后即可获得免费额度体验各种AI模型。"
    },
    {
        "category": "账户与注册",
        "question": "注册后有免费额度吗？",
        "answer": "有的。新注册用户会获得免费体验额度，可以用来调用各种AI模型API，包括Claude、GPT、Gemini等。具体额度以官网显示为准。"
    },
    {
        "category": "账户与注册",
        "question": "如何获取API Key？",
        "answer": "登录接口AI官网后，进入「API密钥」页面，点击「创建新密钥」即可生成。请妥善保管您的API Key，不要泄露给他人。"
    },
    {
        "category": "账户与注册",
        "question": "忘记密码怎么办？",
        "answer": "在登录页面点击「忘记密码」，通过注册时使用的手机号进行验证码验证，即可重置密码。"
    },
    # 二、充值与计费
    {
        "category": "充值与计费",
        "question": "如何充值？",
        "answer": "登录官网后，进入「充值」页面，支持支付宝、微信支付等方式。充值后余额立即到账，可以立即使用。"
    },
    {
        "category": "充值与计费",
        "question": "计费方式是什么？",
        "answer": "按token用量计费（即按实际使用量付费），不同模型价格不同。具体价格可在官网「模型列表」页面查看每个模型的输入/输出价格。"
    },
    {
        "category": "充值与计费",
        "question": "充值后余额可以退款吗？",
        "answer": "一般情况下充值后不支持退款。建议先使用免费额度体验，确认满足需求后再充值。如有特殊情况，请联系客服处理。"
    },
    {
        "category": "充值与计费",
        "question": "如何查看消费记录？",
        "answer": "登录官网后，在「用量统计」页面可以查看详细的API调用记录和消费明细，包括每次调用的模型、token数量和费用。"
    },
    # 三、API调用
    {
        "category": "API调用",
        "question": "接口AI的API地址是什么？",
        "answer": "接口AI的API基础地址为：\n- OpenAI兼容格式：`https://api.jiekou.ai/openai`\n- Anthropic格式：`https://api.jiekou.ai/anthropic`\n\n使用时将对应SDK的base_url设置为以上地址即可。"
    },
    {
        "category": "API调用",
        "question": "支持哪些AI模型？",
        "answer": "接口AI支持100+主流AI模型，包括：\n- **Claude系列**：Claude Opus、Sonnet、Haiku\n- **GPT系列**：GPT-4o、GPT-4、GPT-3.5\n- **Gemini系列**：Gemini Pro、Gemini Flash\n- **开源模型**：Qwen、Llama、Mistral等\n- **图像模型**：FLUX、Stable Diffusion、DALL-E\n- **视频模型**：Kling、Vidu等\n\n完整列表请查看官网模型页面。"
    },
    {
        "category": "API调用",
        "question": "如何使用OpenAI SDK调用接口AI？",
        "answer": "只需修改base_url和api_key即可：\n\n```python\nfrom openai import OpenAI\n\nclient = OpenAI(\n    base_url=\"https://api.jiekou.ai/openai/v1\",\n    api_key=\"你的接口AI API Key\"\n)\n\nresponse = client.chat.completions.create(\n    model=\"claude-sonnet-4-5-20250929\",\n    messages=[{\"role\": \"user\", \"content\": \"你好\"}]\n)\nprint(response.choices[0].message.content)\n```"
    },
    {
        "category": "API调用",
        "question": "如何使用Anthropic SDK调用？",
        "answer": "修改base_url即可：\n\n```python\nfrom anthropic import Anthropic\n\nclient = Anthropic(\n    base_url=\"https://api.jiekou.ai/anthropic\",\n    api_key=\"你的接口AI API Key\"\n)\n\nmessage = client.messages.create(\n    model=\"claude-sonnet-4-5-20250929\",\n    max_tokens=1024,\n    messages=[{\"role\": \"user\", \"content\": \"你好\"}]\n)\nprint(message.content[0].text)\n```"
    },
    {
        "category": "API调用",
        "question": "调用API报错401怎么办？",
        "answer": "HTTP 401表示认证失败，请检查：\n1. API Key是否正确（是否有多余的空格）\n2. API Key是否已过期或被禁用\n3. 账户余额是否充足\n4. base_url是否正确配置\n\n如仍有问题，请重新生成一个API Key尝试。"
    },
    {
        "category": "API调用",
        "question": "调用API报错429怎么办？",
        "answer": "HTTP 429表示请求频率过高（Rate Limit），建议：\n1. 降低请求频率，添加适当的延时\n2. 使用指数退避重试策略\n3. 如需更高并发，请联系客服提升限额"
    },
    # 四、工具集成
    {
        "category": "工具集成",
        "question": "如何在VSCode中使用接口AI？",
        "answer": "通过Claude Code或其他AI插件配置：\n1. 安装Claude Code扩展\n2. 设置环境变量：\n   - `ANTHROPIC_BASE_URL=https://api.jiekou.ai/anthropic`\n   - `ANTHROPIC_API_KEY=你的API Key`\n3. 重启VSCode即可使用\n\n也可以在settings.json中配置OpenAI兼容的插件，将base_url设为 `https://api.jiekou.ai/openai/v1`。"
    },
    {
        "category": "工具集成",
        "question": "如何在Cursor中使用接口AI？",
        "answer": "Cursor支持自定义API端点：\n1. 打开Cursor设置 → Models\n2. 将API Base URL设置为 `https://api.jiekou.ai/openai/v1`\n3. 填入接口AI的API Key\n4. 选择模型（如claude-sonnet-4-5-20250929）\n\n即可在Cursor中使用接口AI提供的各种模型。"
    },
    {
        "category": "工具集成",
        "question": "如何在其他工具中使用接口AI？",
        "answer": "大多数支持OpenAI API格式的工具都可以接入接口AI，通用配置方式：\n1. 找到工具的API设置\n2. 将Base URL设为 `https://api.jiekou.ai/openai/v1`\n3. 填入接口AI的API Key\n4. 模型名称使用接口AI支持的模型ID\n\n支持的工具包括但不限于：ChatBox、NextChat、LobeChat、Open WebUI等。"
    },
    # 五、模型相关
    {
        "category": "模型相关",
        "question": "各模型之间有什么区别？",
        "answer": "不同模型各有特点：\n- **Claude Opus**：最强推理能力，适合复杂分析和编程\n- **Claude Sonnet**：性价比最高，速度和质量平衡\n- **Claude Haiku**：最快速度，适合简单任务\n- **GPT-4o**：多模态能力强，支持图片理解\n- **Gemini**：长上下文支持好，支持100万token\n\n建议根据具体场景选择合适的模型。"
    },
    {
        "category": "模型相关",
        "question": "模型的上下文长度是多少？",
        "answer": "不同模型上下文长度不同：\n- Claude系列：最高200K tokens\n- GPT-4o：128K tokens\n- Gemini Pro：1M tokens（100万）\n- GPT-3.5：16K tokens\n\n具体以官网模型详情页显示为准。注意：上下文越长，单次调用费用越高。"
    },
    {
        "category": "模型相关",
        "question": "支持图片/多模态输入吗？",
        "answer": "支持。以下模型支持图片输入（多模态）：\n- Claude Opus/Sonnet/Haiku（支持图片理解）\n- GPT-4o（支持图片理解）\n- Gemini Pro Vision\n\n使用方式：在API调用时，将图片以base64编码或URL形式传入messages即可。"
    },
    # 六、技术支持
    {
        "category": "技术支持",
        "question": "如何联系客服？",
        "answer": "您可以通过以下方式联系我们：\n- 官网在线客服\n- 微信客服（扫描官网二维码添加）\n- 邮件支持\n\n工作日响应时间通常在1小时内。"
    },
    {
        "category": "技术支持",
        "question": "有技术文档吗？",
        "answer": "有的。完整技术文档请访问：https://docs.jiekou.ai\n\n文档包含：\n- 快速开始指南\n- API参考\n- 各模型详细说明\n- 代码示例（Python、JavaScript、cURL等）\n- 常见问题解答"
    },
    {
        "category": "技术支持",
        "question": "API响应速度慢怎么办？",
        "answer": "如果API响应较慢，可以尝试：\n1. 使用更快的模型（如Haiku或GPT-3.5）\n2. 减少max_tokens参数\n3. 缩短输入内容长度\n4. 使用流式输出（stream=true）提升体验\n5. 检查网络连接是否正常\n\n如持续缓慢，请联系客服反馈。"
    },
    # 七、安全与合规
    {
        "category": "安全与合规",
        "question": "数据安全如何保障？",
        "answer": "接口AI重视数据安全：\n- 所有API通信使用HTTPS加密\n- 不会存储或训练用户的对话数据\n- API Key加密存储\n- 符合相关数据保护法规\n\n建议您也做好安全措施：不要在代码中明文存储API Key，使用环境变量管理敏感信息。"
    },
    {
        "category": "安全与合规",
        "question": "有内容审核限制吗？",
        "answer": "是的。所有API调用均需遵守相关法律法规和平台使用条款。禁止使用AI生成违法、有害或不当内容。违反规定可能导致账户被封禁。"
    },
    {
        "category": "安全与合规",
        "question": "可以用于商业项目吗？",
        "answer": "可以。接口AI的API服务支持商业使用。您可以将其集成到自己的产品、应用或服务中。建议查看官网的服务协议了解详细的使用条款。"
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
