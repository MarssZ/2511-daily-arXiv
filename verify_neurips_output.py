"""验证 NeurIPS 爬虫输出数据质量"""
import json
import sys

def verify_jsonl(filepath):
    """验证 JSONL 文件的数据质量"""
    with open(filepath, encoding='utf-8') as f:
        items = [json.loads(line) for line in f]

    print(f"📊 总计: {len(items)} 篇论文\n")

    # 必需字段
    required_fields = ['id', 'title', 'authors', 'summary', 'abs', 'pdf', 'categories', 'source']

    for idx, item in enumerate(items, 1):
        print(f"{'='*80}")
        print(f"论文 {idx}: {item.get('id', 'MISSING ID')}")
        print(f"{'='*80}")

        # 验证必需字段
        missing_fields = [field for field in required_fields if field not in item]
        if missing_fields:
            print(f"❌ 缺失字段: {missing_fields}")
            continue
        else:
            print(f"✅ 所有必需字段存在")

        # 验证字段类型
        errors = []
        if not isinstance(item['authors'], list):
            errors.append(f"authors 应为数组，实际为 {type(item['authors'])}")
        if not isinstance(item['categories'], list):
            errors.append(f"categories 应为数组，实际为 {type(item['categories'])}")
        if item['source'] != 'neurips':
            errors.append(f"source 应为 'neurips'，实际为 '{item['source']}'")
        if item['comment'] is not None and not isinstance(item['comment'], str):
            errors.append(f"comment 应为 null 或字符串")

        if errors:
            print(f"❌ 类型错误:")
            for error in errors:
                print(f"   - {error}")
        else:
            print(f"✅ 所有字段类型正确")

        # 验证 ID 格式
        if item['id'].startswith('neurips2024_oral_'):
            print(f"✅ ID 格式正确: {item['id']}")
        else:
            print(f"❌ ID 格式错误: {item['id']}")

        # 显示关键信息
        print(f"\n标题: {item['title'][:80]}...")
        print(f"作者数: {len(item['authors'])}")
        print(f"摘要长度: {len(item['summary'])} 字符")
        print(f"PDF 链接: {item['pdf'] if item['pdf'] else '（无）'}")
        print()

    # 统计 PDF 缺失情况
    no_pdf_count = sum(1 for item in items if not item.get('pdf'))
    print(f"\n{'='*80}")
    print(f"📈 统计:")
    print(f"{'='*80}")
    print(f"✅ 成功爬取: {len(items)} 篇")
    print(f"⚠️  缺少 PDF: {no_pdf_count} 篇 ({no_pdf_count/len(items)*100:.1f}%)")
    print(f"✅ 包含 PDF: {len(items) - no_pdf_count} 篇 ({(len(items) - no_pdf_count)/len(items)*100:.1f}%)")

    print(f"\n✨ 验证完成！")

if __name__ == "__main__":
    verify_jsonl('daily_arxiv/test-5.jsonl')
