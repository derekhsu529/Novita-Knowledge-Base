"""
FAQ 种子数据 - Novita AI
来源: FAQ-Novita.pdf (38条中文原文)
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "qa.db"

FAQ_DATA = [
    # 一、账户与计费类 (Q1-Q7)
    {
        "category": "账户与计费",
        "question": "如何删除我的账户？",
        "answer": "提供您的Novita账户ID或邮箱，我们将在14天内删除您的账户。"
    },
    {
        "category": "账户与计费",
        "question": "账户余额为负时能否使用Coding Plan？",
        "answer": "不能。账户余额必须大于0才能使用Coding Plan，即使您已购买套餐。"
    },
    {
        "category": "账户与计费",
        "question": "为什么我的$1代金券消失了？",
        "answer": "系统检测到异常注册活动（如恶意注册、同一设备多账号等）会自动撤销代金券。如确认正常使用，可联系客服重新发放。"
    },
    {
        "category": "账户与计费",
        "question": "如何修改账户邮箱？",
        "answer": "提供原邮箱和新邮箱，客服可协助修改。"
    },
    {
        "category": "账户与计费",
        "question": "支持哪些支付方式？",
        "answer": "支持信用卡（Stripe）、PayPal（需7个工作日手动处理）。不支持加密货币。"
    },
    {
        "category": "账户与计费",
        "question": "如何查看发票？",
        "answer": "支付成功后收据链接30天内有效。如过期，可联系客服提供订单号重新发送。"
    },
    {
        "category": "账户与计费",
        "question": "充值后能否退款？",
        "answer": "一般情况下不支持退款。特殊情况下（如服务完全不可用）可申请退款，通常在每月10-15日处理。"
    },
    # 二、LLM API使用类 (Q8-Q17)
    {
        "category": "LLM API",
        "question": "Coding Plan的扣费顺序是怎样的？",
        "answer": "优先扣除Coding Plan额度，用尽后才扣除API账户余额。"
    },
    {
        "category": "LLM API",
        "question": "套餐内50M Token是如何计算的？",
        "answer": "按基础费率等效Token计算，不同模型价格不同，具体权重取决于价格比例。输入/输出Token均计入。"
    },
    {
        "category": "LLM API",
        "question": "缓存Token如何计费？",
        "answer": "缓存读取Token有单独价格，约为普通输入Token的1/10（具体视模型而定）。缓存写入按正常输入计费。"
    },
    {
        "category": "LLM API",
        "question": "如何提升RPM（每分钟请求数）限制？",
        "answer": "自动升级：根据近3个月充值金额自动提升等级（T1-T5）。\n手动申请：联系客服，根据实际使用量调整。"
    },
    {
        "category": "LLM API",
        "question": "哪些模型支持1M上下文？",
        "answer": "pa/claude-sonnet-4-6 和 pa/claude-opus-4-6 支持1M上下文，使用方式与Claude Sonnet 4.5相同，需添加header `anthropic-beta: context-1m-2025-08-07`。"
    },
    {
        "category": "LLM API",
        "question": "如何关闭模型的思考模式（thinking）？",
        "answer": "Kimi K2.5：使用参数 `\"enable_thinking\": false`\nMiniMax M2.5：暂不支持关闭思考模式"
    },
    {
        "category": "LLM API",
        "question": "为什么调用某些模型报403错误？",
        "answer": "可能原因：1) 余额不足；2) 模型需要加白名单（如Claude系列）；3) 使用了套餐外模型。"
    },
    {
        "category": "LLM API",
        "question": "是否支持top_logprobs参数？",
        "answer": "目前可能不支持该参数。"
    },
    {
        "category": "LLM API",
        "question": "是否支持结构化输出（structured outputs）？",
        "answer": "目前仅支持 `\"type\": \"json_object\"`，不支持 `\"type\": \"json_schema\"`。"
    },
    {
        "category": "LLM API",
        "question": "为什么我的请求报400错误？",
        "answer": "常见原因：输入长度超过模型上下文限制、参数格式错误、缺少必填字段等。可提供trace_id给客服查询。"
    },
    # 三、GPU实例类 (Q18-Q25)
    {
        "category": "GPU实例",
        "question": "如何创建多GPU实例（如5x A100）？",
        "answer": "在创建页面直接选择GPU数量即可。"
    },
    {
        "category": "GPU实例",
        "question": "实例无法启动怎么办？",
        "answer": "尝试迁移实例；如无迁移选项，联系客服处理。"
    },
    {
        "category": "GPU实例",
        "question": "SSH连接失败但实例状态正常？",
        "answer": "可能是本地VSCode配置问题，尝试用终端直接SSH连接。"
    },
    {
        "category": "GPU实例",
        "question": "实例停止后数据保留多久？",
        "answer": "停止状态的实例数据保留7天，期间按$0.005/GB/天收取存储费。7天后自动删除且无法恢复。"
    },
    {
        "category": "GPU实例",
        "question": "能否通过API启动/停止Web Terminal？",
        "answer": "目前不支持，只能通过控制台手动操作。"
    },
    {
        "category": "GPU实例",
        "question": "如何扩容本地存储？",
        "answer": "联系客服提供实例IP和所需容量（如30TB/60TB），获取报价。"
    },
    {
        "category": "GPU实例",
        "question": "月付实例能否更换IP/URL？",
        "answer": "不支持直接更换。如需新实例，需先退订当前月付实例。"
    },
    {
        "category": "GPU实例",
        "question": "为什么下载速度很慢？",
        "answer": "检查是否使用了国内镜像源（如清华源）。海外服务器建议使用官方源。"
    },
    # 四、图像/视频生成类 (Q26-Q30)
    {
        "category": "图像/视频生成",
        "question": "Flux 2 Pro API报错\"failed to exec task\"怎么办？",
        "answer": "可能是内容审核触发或资源不足。检查提示词是否包含敏感内容，或联系客服确认资源状态。"
    },
    {
        "category": "图像/视频生成",
        "question": "如何禁用NSFW过滤？",
        "answer": "WAN2.2 I2V模型：在请求头中添加 `X-DashScope-DataInspection: {\"input\": \"disable\", \"output\": \"disable\"}`"
    },
    {
        "category": "图像/视频生成",
        "question": "Seedream 4.5支持哪些尺寸？",
        "answer": "最小尺寸为1920x1920（约368万像素），不支持更小尺寸。"
    },
    {
        "category": "图像/视频生成",
        "question": "为什么视频生成任务失败报500错误？",
        "answer": "常见原因：参数错误（如video_url为空）、资源不足、官方服务波动。建议检查请求体完整性。"
    },
    {
        "category": "图像/视频生成",
        "question": "Kling Motion Control计费问题？",
        "answer": "计费基于实际使用时长，无额外基础费用。如费用异常，提供账户信息给客服核查。"
    },
    # 五、Serverless类 (Q31-Q33)
    {
        "category": "Serverless",
        "question": "Serverless端点初始化状态持续很久？",
        "answer": "检查日志是否有错误；如资源不足（如L40S库存不足），建议切换到sync端点或其他区域。"
    },
    {
        "category": "Serverless",
        "question": "如何查看Serverless日志？",
        "answer": "目前不支持编程方式流式查看日志，只能通过控制台查看。"
    },
    {
        "category": "Serverless",
        "question": "能否在不同区域查看GPU可用性？",
        "answer": "目前无法直接查看各区域GPU库存，可尝试创建或联系客服确认。"
    },
    # 六、其他常见问题 (Q34-Q38)
    {
        "category": "其他",
        "question": "是否支持ComfyUI？",
        "answer": "GPU支持ComfyUI，镜像仓库提供相关镜像，也可上传自定义镜像。"
    },
    {
        "category": "其他",
        "question": "如何托管OpenClaw？",
        "answer": "Novita已上线ClawDBot模板，可直接在Sandbox中启动。"
    },
    {
        "category": "其他",
        "question": "企业级需求（如H100集群）如何对接？",
        "answer": "提供公司名称、业务场景、需求量、联系方式，客户经理将直接对接。"
    },
    {
        "category": "其他",
        "question": "如何申请模型白名单？",
        "answer": "联系客服提供账户信息和所需模型名称。"
    },
    {
        "category": "其他",
        "question": "API返回\"server overload\"怎么办？",
        "answer": "通常是临时资源压力，建议稍后重试或联系客服确认。"
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
