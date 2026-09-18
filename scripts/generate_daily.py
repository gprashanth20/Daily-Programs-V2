#!/usr/bin/env python3
"""
Pops 2 topics off queue.json, writes a Java file for each under programs/<category>/,
moves the topic into history.json, and updates queue.json.

Run with no arguments. Designed to be called by the GitHub Actions workflow,
but works fine run locally too: `python3 scripts/generate_daily.py`
"""
import json
import os
import re
import sys
from datetime import date, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE_PATH = os.path.join(ROOT, "queue.json")
HISTORY_PATH = os.path.join(ROOT, "history.json")
PROGRAMS_DIR = os.path.join(ROOT, "programs")

PER_DAY = 2

# Real, runnable implementations for common topics. Add more anytime -
# match is case-insensitive substring against the topic title.
TEMPLATES = {
    "binary search": '''public class {cls} {{
    // Iterative binary search - O(log n)
    static int search(int[] arr, int target) {{
        int lo = 0, hi = arr.length - 1;
        while (lo <= hi) {{
            int mid = lo + (hi - lo) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }}
        return -1;
    }}

    // Recursive version
    static int searchRecursive(int[] arr, int lo, int hi, int target) {{
        if (lo > hi) return -1;
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == target) return mid;
        return arr[mid] < target
            ? searchRecursive(arr, mid + 1, hi, target)
            : searchRecursive(arr, lo, mid - 1, target);
    }}

    public static void main(String[] args) {{
        int[] data = {{2, 5, 8, 12, 16, 23, 38, 45, 56, 72}};
        System.out.println("Iterative: index of 23 -> " + search(data, 23));
        System.out.println("Recursive: index of 45 -> " + searchRecursive(data, 0, data.length - 1, 45));
        System.out.println("Missing value -> " + search(data, 99));
    }}
}}
''',
    "bubble sort": '''public class {cls} {{
    static void sort(int[] arr) {{
        int n = arr.length;
        for (int i = 0; i < n - 1; i++) {{
            boolean swapped = false;
            for (int j = 0; j < n - i - 1; j++) {{
                if (arr[j] > arr[j + 1]) {{
                    int tmp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = tmp;
                    swapped = true;
                }}
            }}
            if (!swapped) break; // already sorted
        }}
    }}

    public static void main(String[] args) {{
        int[] data = {{5, 1, 4, 2, 8, 0, 9, 3}};
        sort(data);
        System.out.println(java.util.Arrays.toString(data));
    }}
}}
''',
    "merge sort": '''public class {cls} {{
    static void sort(int[] arr, int lo, int hi) {{
        if (lo >= hi) return;
        int mid = lo + (hi - lo) / 2;
        sort(arr, lo, mid);
        sort(arr, mid + 1, hi);
        merge(arr, lo, mid, hi);
    }}

    static void merge(int[] arr, int lo, int mid, int hi) {{
        int[] left = java.util.Arrays.copyOfRange(arr, lo, mid + 1);
        int[] right = java.util.Arrays.copyOfRange(arr, mid + 1, hi + 1);
        int i = 0, j = 0, k = lo;
        while (i < left.length && j < right.length) {{
            arr[k++] = left[i] <= right[j] ? left[i++] : right[j++];
        }}
        while (i < left.length) arr[k++] = left[i++];
        while (j < right.length) arr[k++] = right[j++];
    }}

    public static void main(String[] args) {{
        int[] data = {{38, 27, 43, 3, 9, 82, 10}};
        sort(data, 0, data.length - 1);
        System.out.println(java.util.Arrays.toString(data));
    }}
}}
''',
    "quick sort": '''public class {cls} {{
    static void sort(int[] arr, int lo, int hi) {{
        if (lo >= hi) return;
        int p = partition(arr, lo, hi);
        sort(arr, lo, p - 1);
        sort(arr, p + 1, hi);
    }}

    static int partition(int[] arr, int lo, int hi) {{
        int pivot = arr[hi];
        int i = lo - 1;
        for (int j = lo; j < hi; j++) {{
            if (arr[j] < pivot) {{
                i++;
                int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
            }}
        }}
        int tmp = arr[i + 1]; arr[i + 1] = arr[hi]; arr[hi] = tmp;
        return i + 1;
    }}

    public static void main(String[] args) {{
        int[] data = {{10, 7, 8, 9, 1, 5}};
        sort(data, 0, data.length - 1);
        System.out.println(java.util.Arrays.toString(data));
    }}
}}
''',
    "fibonacci": '''import java.util.HashMap;
import java.util.Map;

public class {cls} {{
    static final Map<Integer, Long> memo = new HashMap<>();

    static long fib(int n) {{
        if (n <= 1) return n;
        if (memo.containsKey(n)) return memo.get(n);
        long result = fib(n - 1) + fib(n - 2);
        memo.put(n, result);
        return result;
    }}

    public static void main(String[] args) {{
        for (int i = 0; i <= 20; i++) {{
            System.out.print(fib(i) + " ");
        }}
        System.out.println();
    }}
}}
''',
    "two sum": '''import java.util.HashMap;
import java.util.Map;

public class {cls} {{
    static int[] twoSum(int[] nums, int target) {{
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {{
            int complement = target - nums[i];
            if (seen.containsKey(complement)) {{
                return new int[] {{ seen.get(complement), i }};
            }}
            seen.put(nums[i], i);
        }}
        throw new IllegalArgumentException("No two sum solution");
    }}

    public static void main(String[] args) {{
        int[] nums = {{2, 7, 11, 15}};
        int[] idx = twoSum(nums, 9);
        System.out.println("Indices: " + idx[0] + ", " + idx[1]);
    }}
}}
''',
    "singleton": '''public class {cls} {{
    private static volatile {cls} instance;
    private int value;

    private {cls}() {{
        value = 0;
    }}

    public static {cls} getInstance() {{
        if (instance == null) {{
            synchronized ({cls}.class) {{
                if (instance == null) {{
                    instance = new {cls}();
                }}
            }}
        }}
        return instance;
    }}

    public void increment() {{ value++; }}
    public int getValue() {{ return value; }}

    public static void main(String[] args) {{
        {cls} a = {cls}.getInstance();
        {cls} b = {cls}.getInstance();
        a.increment();
        b.increment();
        System.out.println("Shared value: " + a.getValue());
        System.out.println("Same instance: " + (a == b));
    }}
}}
''',
    "stack using array": '''public class {cls} {{
    private final int[] data;
    private int top = -1;

    public {cls}(int capacity) {{
        data = new int[capacity];
    }}

    public void push(int value) {{
        if (top == data.length - 1) throw new RuntimeException("Stack overflow");
        data[++top] = value;
    }}

    public int pop() {{
        if (top == -1) throw new RuntimeException("Stack underflow");
        return data[top--];
    }}

    public boolean isEmpty() {{ return top == -1; }}

    public static void main(String[] args) {{
        {cls} stack = new {cls}(5);
        stack.push(1);
        stack.push(2);
        stack.push(3);
        while (!stack.isEmpty()) {{
            System.out.println(stack.pop());
        }}
    }}
}}
''',
    "heap sort": '''public class {cls} {{
    static void sort(int[] arr) {{
        int n = arr.length;
        for (int i = n / 2 - 1; i >= 0; i--) heapify(arr, n, i);
        for (int i = n - 1; i > 0; i--) {{
            int tmp = arr[0]; arr[0] = arr[i]; arr[i] = tmp;
            heapify(arr, i, 0);
        }}
    }}

    static void heapify(int[] arr, int n, int i) {{
        int largest = i, left = 2 * i + 1, right = 2 * i + 2;
        if (left < n && arr[left] > arr[largest]) largest = left;
        if (right < n && arr[right] > arr[largest]) largest = right;
        if (largest != i) {{
            int tmp = arr[i]; arr[i] = arr[largest]; arr[largest] = tmp;
            heapify(arr, n, largest);
        }}
    }}

    public static void main(String[] args) {{
        int[] data = {{12, 11, 13, 5, 6, 7}};
        sort(data);
        System.out.println(java.util.Arrays.toString(data));
    }}
}}
''',
    "linked list reversal": '''public class {cls} {{
    static class Node {{
        int value;
        Node next;
        Node(int value) {{ this.value = value; }}
    }}

    static Node reverse(Node head) {{
        Node prev = null;
        while (head != null) {{
            Node next = head.next;
            head.next = prev;
            prev = head;
            head = next;
        }}
        return prev;
    }}

    static void print(Node head) {{
        StringBuilder sb = new StringBuilder();
        while (head != null) {{
            sb.append(head.value).append(" -> ");
            head = head.next;
        }}
        sb.append("null");
        System.out.println(sb);
    }}

    public static void main(String[] args) {{
        Node head = new Node(1);
        head.next = new Node(2);
        head.next.next = new Node(3);
        head.next.next.next = new Node(4);
        print(head);
        head = reverse(head);
        print(head);
    }}
}}
''',
}

GENERIC_TEMPLATE = '''/**
 * Topic     : {title}
 * Category  : {category}
 * Notes     : {notes}
 * Date      : {date}
 *
 * TODO: replace this scaffold with a real implementation.
 * Structure kept deliberately simple so it compiles as-is and can be
 * filled in without fighting the boilerplate.
 */
public class {cls} {{

    static void solve() {{
        // TODO: implement {title}
        System.out.println("TODO: implement {title}");
    }}

    public static void main(String[] args) {{
        System.out.println("=== {title} ({category}) ===");
        solve();
    }}
}}
'''


def slug_to_class_name(title: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9 ]", "", title)
    return "".join(word.capitalize() for word in cleaned.split())


def category_to_dirname(category: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", category.strip().lower()).strip("-")


def pick_template(title: str) -> str:
    lower = title.lower()
    for key, tpl in TEMPLATES.items():
        if key in lower:
            return tpl
    return None


def main():
    with open(QUEUE_PATH) as f:
        queue_data = json.load(f)
    with open(HISTORY_PATH) as f:
        history_data = json.load(f)

    queue = queue_data.get("queue", [])
    if not queue:
        print("Queue is empty - nothing to generate. Add topics to queue.json.")
        return 0

    today = date.today().isoformat()
    picked = queue[:PER_DAY]
    remaining = queue[PER_DAY:]

    written = []
    for entry in picked:
        title = entry["title"]
        category = entry.get("category", "General")
        notes = entry.get("notes", "") or "-"
        cls = slug_to_class_name(title)
        dirname = category_to_dirname(category)
        target_dir = os.path.join(PROGRAMS_DIR, dirname)
        os.makedirs(target_dir, exist_ok=True)

        tpl = pick_template(title)
        if tpl:
            content = tpl.format(cls=cls)
        else:
            content = GENERIC_TEMPLATE.format(
                title=title, category=category, notes=notes, date=today, cls=cls
            )

        file_path = os.path.join(target_dir, f"{cls}.java")
        # Avoid overwriting if somehow already present (manual re-runs, retries)
        if os.path.exists(file_path):
            file_path = os.path.join(target_dir, f"{cls}_{today}.java")

        with open(file_path, "w") as f:
            f.write(content)

        rel_path = os.path.relpath(file_path, ROOT)
        written.append(rel_path)
        entry["completed_on"] = today
        entry["file"] = rel_path
        history_data.setdefault("completed", []).append(entry)
        print(f"Wrote {rel_path}")

    queue_data["queue"] = remaining
    with open(QUEUE_PATH, "w") as f:
        json.dump(queue_data, f, indent=2)
    with open(HISTORY_PATH, "w") as f:
        json.dump(history_data, f, indent=2)

    if remaining:
        print(f"{len(remaining)} topic(s) left in queue.")
    else:
        print("Queue is now empty - add more topics to queue.json before the next run.")

    # Emit file list for the workflow's commit message
    marker_path = os.path.join(ROOT, ".last_run_files.txt")
    with open(marker_path, "w") as f:
        f.write("\n".join(written))

    return 0


if __name__ == "__main__":
    sys.exit(main())
