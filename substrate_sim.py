# substrate_sim_fast.py - 解析解版本

import numpy as np

class SubstrateSystemFast:
    def __init__(self, 
                 initial_deficit=1.0,
                 net_growth_rate=1e-30):  # 每秒净增长率
        
        self.initial_deficit = initial_deficit
        self.net_growth_rate = net_growth_rate
    
    def calculate_deficit(self, time_seconds):
        """
        解析解：S(t) = S0 + ε × t
        """
        return self.initial_deficit + self.net_growth_rate * time_seconds
    
    def run_cosmic_timeline(self):
        """
        直接计算关键时间点
        """
        print("="*80)
        print("COSMIC TIMELINE - ANALYTICAL SOLUTION")
        print("="*80)
        print(f"Initial deficit: {self.initial_deficit:.20e}")
        print(f"Net growth rate: {self.net_growth_rate:.2e}/s")
        print("="*80)
        
        # 定义关键时间点
        timeline = [
            (0, "Big Bang"),
            (380000, "CMB formation"),
            (3.154e13, "1 million years"),
            (3.154e15, "100 million years"),
            (3.154e16, "1 billion years"),
            (1.577e17, "5 billion years"),
            (4.35e17, "13.8 billion years (now)"),
            (1e18, "31.7 billion years"),
            (1e19, "317 billion years"),
            (1e20, "3.17 trillion years"),
        ]
        
        print("\n{:<25} {:<20} {:<25} {:<15}".format(
            "Time", "Seconds", "Deficit", "Growth (%)"))
        print("-"*80)
        
        for seconds, label in timeline:
            deficit = self.calculate_deficit(seconds)
            growth_pct = (deficit - self.initial_deficit) / self.initial_deficit * 100
            
            # 格式化时间显示
            if seconds < 3.154e7:
                time_str = f"{seconds/3.154e7:.2e} years"
            elif seconds < 3.154e10:
                time_str = f"{seconds/3.154e7:.2f} million years"
            elif seconds < 3.154e13:
                time_str = f"{seconds/3.154e10:.2f} billion years"
            else:
                time_str = f"{seconds/3.154e13:.2f} trillion years"
            
            print("{:<25} {:<20.2e} {:<25.20e} {:<15.2e}".format(
                time_str, seconds, deficit, growth_pct))
        
        print("="*80)
        print("\n✓ Simulation completed in milliseconds!")
        print("="*80)

# 运行
if __name__ == "__main__":
    system = SubstrateSystemFast(
        initial_deficit=1.0,
        net_growth_rate=1e-30
    )
    system.run_cosmic_timeline()
