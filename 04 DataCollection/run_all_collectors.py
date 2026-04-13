#!/usr/bin/env python3
"""
统一数据采集运行脚本
功能：运行所有数据采集器
优先级：P1
"""

import subprocess
import sys
import os
from datetime import datetime

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)


class CollectorRunner:
    """采集器运行器"""

    def __init__(self):
        self.collectors = {
            "policy_collector": {
                "name": "政策法规采集器",
                "script": os.path.join(SCRIPT_DIR, "collectors", "policy_collector.py"),
                "priority": "P0",
                "enabled": True
            },
            "customer_collector": {
                "name": "客户画像采集器",
                "script": os.path.join(SCRIPT_DIR, "collectors", "customer_collector.py"),
                "priority": "P0",
                "enabled": True
            },
            "supply_chain_discoverer": {
                "name": "供应链关系发现器",
                "script": os.path.join(SCRIPT_DIR, "collectors", "supply_chain_discoverer.py"),
                "priority": "P0",
                "enabled": True
            }
        }

    def run_all(self):
        """运行所有采集器"""
        print("="*80)
        print("统一数据采集运行脚本")
        print("="*80)
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        results = {}

        for collector_id, collector_info in self.collectors.items():
            if not collector_info["enabled"]:
                print(f"⏭️  跳过: {collector_info['name']} (未启用)")
                continue

            print(f"\n{'='*80}")
            print(f"运行: {collector_info['name']} ({collector_info['priority']})")
            print(f"{'='*80}\n")

            try:
                result = self.run_collector(collector_id, collector_info)
                results[collector_id] = {
                    "success": True,
                    "message": "采集成功"
                }
                print(f"\n✅ {collector_info['name']} 完成")
            except Exception as e:
                results[collector_id] = {
                    "success": False,
                    "message": str(e)
                }
                print(f"\n✗ {collector_info['name']} 失败: {str(e)}")

        # 生成总结报告
        self.generate_summary(results)

    def run_collector(self, collector_id, collector_info):
        """运行单个采集器"""
        script_path = collector_info["script"]

        if not os.path.exists(script_path):
            raise FileNotFoundError(f"采集器脚本不存在: {script_path}")

        # 运行采集器
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )

        # 打印输出
        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        # 检查返回码
        if result.returncode != 0:
            raise RuntimeError(f"采集器运行失败，返回码: {result.returncode}")

        return result

    def run_single(self, collector_id):
        """运行单个采集器"""
        if collector_id not in self.collectors:
            raise ValueError(f"未知的采集器ID: {collector_id}")

        collector_info = self.collectors[collector_id]

        print("="*80)
        print(f"运行: {collector_info['name']}")
        print("="*80)
        print()

        try:
            self.run_collector(collector_id, collector_info)
            print(f"\n✅ {collector_info['name']} 完成")
        except Exception as e:
            print(f"\n✗ {collector_info['name']} 失败: {str(e)}")
            sys.exit(1)

    def generate_summary(self, results):
        """生成总结报告"""
        print("\n")
        print("="*80)
        print("采集总结报告")
        print("="*80)

        total = len(results)
        success = sum(1 for r in results.values() if r["success"])
        failed = total - success

        print(f"\n总采集器数: {total}")
        print(f"成功: {success}")
        print(f"失败: {failed}")
        print(f"成功率: {success/total*100:.1f}%")

        if failed > 0:
            print("\n失败的采集器:")
            for collector_id, result in results.items():
                if not result["success"]:
                    collector_name = self.collectors[collector_id]["name"]
                    print(f"  - {collector_name}: {result['message']}")

        print(f"\n结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()


def print_usage():
    """打印使用说明"""
    print("""
使用方法:
  python run_all_collectors.py                  # 运行所有采集器
  python run_all_collectors.py policy          # 运行政策采集器
  python run_all_collectors.py customer        # 运行客户采集器
  python run_all_collectors.py supply_chain    # 运行供应链发现器

采集器列表:
  - policy_collector: 政策法规采集器
  - customer_collector: 客户画像采集器
  - supply_chain_discoverer: 供应链关系发现器
""")


if __name__ == "__main__":
    runner = CollectorRunner()

    # 解析命令行参数
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command in ["-h", "--help", "help"]:
            print_usage()
            sys.exit(0)

        # 运行单个采集器
        collector_id = command
        if collector_id not in runner.collectors:
            print(f"错误: 未知的采集器ID: {collector_id}")
            print(f"\n可用的采集器:")
            for cid, info in runner.collectors.items():
                print(f"  - {cid}: {info['name']}")
            sys.exit(1)

        runner.run_single(collector_id)
    else:
        # 运行所有采集器
        runner.run_all()
