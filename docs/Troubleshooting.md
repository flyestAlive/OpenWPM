# Troubleshooting

## Crash on macOS when restarting the browser

On some macOS systems the demo may crash with an error similar to:

```
objc[...]: +[__NSPlaceholderDictionary initialize] may have been inserted by the dynamic linker...
```

This occurs when the browser process is restarted using Python's default `fork` start method for multiprocessing. macOS does not fully support forking processes that use the system GUI frameworks. You can avoid the crash in two ways:

1. Explicitly set the multiprocessing start method to `spawn`:

   ```python
   import multiprocessing
   multiprocessing.set_start_method("spawn")
   ```

   Add this before running `demo.py` or your own script.

2. Alternatively, run OpenWPM inside Docker using the provided Dockerfile or helper scripts. Docker uses a Linux environment where this issue does not occur.

