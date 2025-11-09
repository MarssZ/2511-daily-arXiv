"""验证 AI 增强输出质量"""
import json
import sys

def verify_ai_enhancement(filepath):
    """验证 AI 增强后的 JSONL 文件"""
    with open(filepath, encoding='utf-8') as f:
        items = [json.loads(line) for line in f]

    print(f"📊 总计: {len(items)} 篇论文\n")

    # 检查 AI 字段定义（从 structure.py）
    ai_required_fields = [
        'core_problem', 'key_insight', 'method', 'method_formula',
        'core_finding', 'mechanism_insight', 'action_value',
        'transferability', 'value_score', 'summary_core', 'summary_layman'
    ]

    success_count = 0
    for idx, item in enumerate(items, 1):
        print(f"{'='*80}")
        print(f"论文 {idx}: {item.get('id', 'MISSING ID')}")
        print(f"{'='*80}")

        # 验证原始字段仍然存在
        if 'source' in item and item['source'] == 'neurips':
            print(f"✅ source 字段透传成功: {item['source']}")
        else:
            print(f"❌ source 字段缺失或错误")

        # 验证 AI 字段
        if 'AI' not in item:
            print(f"❌ 缺少 AI 字段")
            continue

        ai_data = item['AI']
        if not isinstance(ai_data, dict):
            print(f"❌ AI 字段类型错误: {type(ai_data)}")
            continue

        # 检查所有必需的 AI 字段
        missing_ai_fields = [field for field in ai_required_fields if field not in ai_data]
        if missing_ai_fields:
            print(f"⚠️  AI 字段不完整，缺少: {missing_ai_fields}")
        else:
            print(f"✅ 所有 AI 字段完整 ({len(ai_required_fields)} 个)")
            success_count += 1

        # 显示部分 AI 内容
        print(f"\n核心问题: {ai_data.get('core_problem', 'N/A')[:100]}...")
        print(f"大白话总结: {ai_data.get('summary_layman', 'N/A')[:100]}...")
        print()

    # 统计
    print(f"{'='*80}")
    print(f"📈 AI 增强统计:")
    print(f"{'='*80}")
    print(f"✅ 成功增强: {success_count}/{len(items)} ({success_count/len(items)*100:.1f}%)")
    print(f"⚠️  部分失败: {len(items) - success_count}/{len(items)}")

    if success_count == len(items):
        print(f"\n🎉 所有论文 AI 增强成功！")
    else:
        print(f"\n⚠️  部分论文 AI 增强不完整")

if __name__ == "__main__":
    verify_ai_enhancement('daily_arxiv/test-5_AI_enhanced_Chinese.jsonl')
