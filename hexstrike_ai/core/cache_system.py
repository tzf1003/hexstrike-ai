#!/usr/bin/env python3
"""
HexStrike AI - 缓存系统
Cache System

这个模块提供了智能缓存功能，包括：
- LRU缓存算法
- TTL过期管理
- 内存使用监控
- 缓存统计分析
"""

import time
import threading
import pickle
import hashlib
from datetime import datetime, timedelta
from typing import Any, Optional, Dict
from collections import OrderedDict

from .base_classes import CacheStats
from ..config.logger_config import get_logger

class AdvancedCache:
    """高级缓存系统"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """初始化缓存系统
        
        Args:
            max_size: 最大缓存条目数
            default_ttl: 默认TTL（秒）
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: OrderedDict = OrderedDict()
        self.access_times: Dict[str, float] = {}
        self.expire_times: Dict[str, float] = {}
        self.hit_count = 0
        self.miss_count = 0
        self.lock = threading.RLock()
        self.logger = get_logger('CacheSystem')
        
        # 启动清理线程
        self._start_cleanup_thread()
        
        self.logger.success(f"💾 缓存系统启动 (最大条目: {max_size}, 默认TTL: {default_ttl}秒)")
    
    def _start_cleanup_thread(self):
        """启动清理线程"""
        def cleanup_worker():
            while True:
                try:
                    self._cleanup_expired()
                    time.sleep(60)  # 每分钟清理一次
                except Exception as e:
                    self.logger.error(f"❌ 缓存清理错误: {e}")
                    time.sleep(60)
        
        cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        cleanup_thread.start()
    
    def _generate_key(self, key: str) -> str:
        """生成缓存键"""
        return hashlib.md5(key.encode()).hexdigest()
    
    def _cleanup_expired(self):
        """清理过期条目"""
        with self.lock:
            current_time = time.time()
            expired_keys = []
            
            for key, expire_time in self.expire_times.items():
                if current_time > expire_time:
                    expired_keys.append(key)
            
            for key in expired_keys:
                self._remove_key(key)
            
            if expired_keys:
                self.logger.debug(f"🧹 清理了 {len(expired_keys)} 个过期缓存条目")
    
    def _remove_key(self, key: str):
        """移除缓存键"""
        self.cache.pop(key, None)
        self.access_times.pop(key, None)
        self.expire_times.pop(key, None)
    
    def _evict_lru(self):
        """移除最少使用的条目"""
        if self.cache:
            # 移除最旧的条目
            oldest_key = next(iter(self.cache))
            self._remove_key(oldest_key)
            self.logger.debug(f"🔄 LRU移除缓存条目: {oldest_key}")
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        cache_key = self._generate_key(key)
        
        with self.lock:
            current_time = time.time()
            
            # 检查是否存在且未过期
            if (cache_key in self.cache and 
                cache_key in self.expire_times and
                current_time <= self.expire_times[cache_key]):
                
                # 更新访问时间
                self.access_times[cache_key] = current_time
                
                # 移到末尾（LRU更新）
                value = self.cache.pop(cache_key)
                self.cache[cache_key] = value
                
                self.hit_count += 1
                return value
            
            # 如果过期，删除
            if cache_key in self.cache:
                self._remove_key(cache_key)
            
            self.miss_count += 1
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """设置缓存值"""
        cache_key = self._generate_key(key)
        ttl = ttl or self.default_ttl
        
        with self.lock:
            current_time = time.time()
            expire_time = current_time + ttl
            
            # 如果已存在，先删除
            if cache_key in self.cache:
                self._remove_key(cache_key)
            
            # 检查容量限制
            while len(self.cache) >= self.max_size:
                self._evict_lru()
            
            # 添加新条目
            self.cache[cache_key] = value
            self.access_times[cache_key] = current_time
            self.expire_times[cache_key] = expire_time
            
            return True
    
    def delete(self, key: str) -> bool:
        """删除缓存值"""
        cache_key = self._generate_key(key)
        
        with self.lock:
            if cache_key in self.cache:
                self._remove_key(cache_key)
                return True
            return False
    
    def clear(self):
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            self.access_times.clear()
            self.expire_times.clear()
            self.logger.info("🧹 缓存已清空")
    
    def get_stats(self) -> CacheStats:
        """获取缓存统计"""
        with self.lock:
            total_requests = self.hit_count + self.miss_count
            hit_rate = (self.hit_count / total_requests) if total_requests > 0 else 0
            
            # 计算内存使用量（估算）
            memory_usage = 0
            try:
                for value in self.cache.values():
                    memory_usage += len(pickle.dumps(value))
            except:
                memory_usage = len(self.cache) * 1024  # 估算值
            
            # 获取最旧和最新条目时间
            oldest_entry = None
            newest_entry = None
            
            if self.access_times:
                oldest_time = min(self.access_times.values())
                newest_time = max(self.access_times.values())
                oldest_entry = datetime.fromtimestamp(oldest_time)
                newest_entry = datetime.fromtimestamp(newest_time)
            
            return CacheStats(
                total_entries=len(self.cache),
                hit_count=self.hit_count,
                miss_count=self.miss_count,
                hit_rate=hit_rate,
                memory_usage=memory_usage,
                oldest_entry=oldest_entry,
                newest_entry=newest_entry
            )