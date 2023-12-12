import os

__all__ = [f[:-3] for f in os.listdir('./days') if f[-3:] == '.py']
