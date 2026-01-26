"""
SLIDING WINDOW TECHNIQUE - Explained for High Schoolers
========================================================

What is a Sliding Window?
-------------------------
Imagine you're looking through a window at a street. You can only see 3 houses at a time.
To see the next houses, you slide the window to the right by one house.

    [House1] [House2] [House3] House4  House5  <- Your window shows houses 1,2,3
     House1  [House2] [House3] [House4] House5  <- Slide right! Now shows 2,3,4
     House1   House2  [House3] [House4] [House5] <- Slide right! Now shows 3,4,5

This is exactly how "sliding window" works in programming!
"""

# ============================================================================
# EXAMPLE 1: Finding the Maximum Sum of 3 Consecutive Numbers
# ============================================================================

def example_1_the_slow_way():
    """
    Let's say you have a list of numbers and want to find the biggest sum
    of any 3 numbers next to each other.

    THE SLOW WAY (Don't do this!):
    For each position, add up 3 numbers from scratch
    """
    numbers = [2, 5, 1, 8, 3, 4, 7]
    window_size = 3
    max_sum = 0

    print("THE SLOW WAY:")
    print(f"Numbers: {numbers}")
    print(f"Finding max sum of {window_size} consecutive numbers\n")

    # We can only go up to position where we have 3 numbers left
    for i in range(len(numbers) - window_size + 1):
        # Add up 3 numbers every single time from scratch
        current_sum = numbers[i] + numbers[i+1] + numbers[i+2]
        print(f"Position {i}: {numbers[i]} + {numbers[i+1]} + {numbers[i+2]} = {current_sum}")

        if current_sum > max_sum:
            max_sum = current_sum

    print(f"\nMaximum sum: {max_sum}")
    print("Problem: We're doing a lot of repeated addition!\n")
    return max_sum


def example_1_the_sliding_window_way():
    """
    THE SMART WAY (Sliding Window):
    Calculate the first sum, then slide!
    When you slide, just subtract the left number and add the new right number!
    """
    numbers = [2, 5, 1, 8, 3, 4, 7]
    window_size = 3

    print("\nTHE SLIDING WINDOW WAY:")
    print(f"Numbers: {numbers}")
    print(f"Finding max sum of {window_size} consecutive numbers\n")

    # STEP 1: Calculate the FIRST window sum
    window_sum = sum(numbers[0:window_size])  # 2 + 5 + 1 = 8
    max_sum = window_sum

    print(f"First window [2, 5, 1]: sum = {window_sum}")

    # STEP 2: Slide the window!
    # Start from position 1 and slide to the right
    for i in range(1, len(numbers) - window_size + 1):
        # Remove the leftmost number from the previous window
        # Add the new rightmost number
        old_left = numbers[i - 1]  # The number we're leaving behind
        new_right = numbers[i + window_size - 1]  # The new number entering the window

        window_sum = window_sum - old_left + new_right

        print(f"Slide to position {i}: Remove {old_left}, Add {new_right} → sum = {window_sum}")

        if window_sum > max_sum:
            max_sum = window_sum

    print(f"\nMaximum sum: {max_sum}")
    print("See? Much faster! We only subtract and add once per slide!\n")
    return max_sum


# ============================================================================
# EXAMPLE 2: Finding Average Temperature (More Visual)
# ============================================================================

def example_2_temperature_averages():
    """
    You recorded temperatures for 7 days.
    Find the highest average temperature for any 3-day period.
    """
    temperatures = [70, 75, 72, 80, 85, 78, 82]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    window_size = 3

    print("\nEXAMPLE 2: Temperature Averages")
    print("=" * 50)

    # Show the temperatures
    for i, temp in enumerate(temperatures):
        print(f"{days[i]}: {temp}°F")

    print(f"\nFinding the best {window_size}-day average:\n")

    # Calculate first window
    window_sum = sum(temperatures[0:window_size])
    max_avg = window_sum / window_size
    best_days = days[0:window_size]

    print(f"Days {days[0]}-{days[2]}: {temperatures[0:3]} → Average: {window_sum/window_size:.1f}°F")

    # Slide the window
    for i in range(1, len(temperatures) - window_size + 1):
        # Slide!
        window_sum = window_sum - temperatures[i-1] + temperatures[i+window_size-1]
        current_avg = window_sum / window_size

        window_temps = temperatures[i:i+window_size]
        print(f"Days {days[i]}-{days[i+2]}: {window_temps} → Average: {current_avg:.1f}°F")

        if current_avg > max_avg:
            max_avg = current_avg
            best_days = days[i:i+window_size]

    print(f"\n🌡️  Best {window_size}-day period: {best_days[0]}-{best_days[2]} with average {max_avg:.1f}°F")


# ============================================================================
# EXAMPLE 3: Finding a Subarray with Exact Sum (Variable Window Size)
# ============================================================================

def example_3_find_sum_variable_window():
    """
    Sometimes the window size can CHANGE!

    Problem: Find a sequence of consecutive numbers that add up to exactly 12
    """
    numbers = [2, 5, 1, 8, 3, 4]
    target_sum = 12

    print("\n\nEXAMPLE 3: Variable Window Size")
    print("=" * 50)
    print(f"Numbers: {numbers}")
    print(f"Find consecutive numbers that sum to {target_sum}\n")

    # Two pointers: left and right edges of our window
    left = 0
    right = 0
    current_sum = numbers[0]

    print("Starting with window at position 0:")
    print(f"Window: [{numbers[left]}], sum = {current_sum}\n")

    while right < len(numbers):
        if current_sum == target_sum:
            # Found it!
            window = numbers[left:right+1]
            print(f"✓ FOUND IT! Window: {window}, sum = {current_sum}")
            return window

        elif current_sum < target_sum:
            # Sum too small? Expand window to the right!
            right += 1
            if right < len(numbers):
                current_sum += numbers[right]
                print(f"Sum too small → Expand right: {numbers[left:right+1]}, sum = {current_sum}")

        else:
            # Sum too big? Shrink window from the left!
            current_sum -= numbers[left]
            left += 1
            if left <= right:
                print(f"Sum too big → Shrink left: {numbers[left:right+1]}, sum = {current_sum}")

    print("No solution found!")
    return None


# ============================================================================
# EXAMPLE 4: Longest Substring Without Repeating Characters
# ============================================================================

def example_4_unique_characters():
    """
    Find the longest sequence of characters with no repeats.

    Example: "abcabcbb"
    Answer: "abc" (length 3)
    """
    text = "abcabcbb"

    print("\n\nEXAMPLE 4: Longest Unique Character Sequence")
    print("=" * 50)
    print(f"Text: '{text}'")
    print("Find longest part with no repeating letters\n")

    left = 0
    max_length = 0
    best_substring = ""
    seen_characters = {}  # Stores character and its position

    for right in range(len(text)):
        current_char = text[right]

        # If we've seen this character before AND it's in our current window
        if current_char in seen_characters and seen_characters[current_char] >= left:
            # Move left pointer to just after the previous occurrence
            print(f"'{current_char}' repeats! Sliding window left...")
            left = seen_characters[current_char] + 1

        # Record where we saw this character
        seen_characters[current_char] = right

        # Check if this is our longest window yet
        current_length = right - left + 1
        current_substring = text[left:right+1]

        print(f"Window: '{current_substring}' (length {current_length})")

        if current_length > max_length:
            max_length = current_length
            best_substring = current_substring

    print(f"\n✓ Longest unique sequence: '{best_substring}' (length {max_length})")
    return best_substring


# ============================================================================
# KEY TAKEAWAYS
# ============================================================================

def print_key_concepts():
    """
    Print the main ideas about sliding window
    """
    print("\n\n" + "=" * 60)
    print("KEY CONCEPTS - SLIDING WINDOW")
    print("=" * 60)

    concepts = [
        "1. WHAT IS IT?",
        "   A way to look at consecutive elements in a sequence",
        "   Instead of recalculating everything, we REUSE previous work",
        "",
        "2. TWO TYPES:",
        "   • FIXED SIZE: Window stays same size (Example 1 & 2)",
        "   • VARIABLE SIZE: Window grows/shrinks (Example 3 & 4)",
        "",
        "3. WHY USE IT?",
        "   Makes your code MUCH FASTER!",
        "   Instead of recalculating everything, you just update the edges",
        "",
        "4. THE PATTERN:",
        "   • Calculate the first window",
        "   • Slide the window (remove left, add right)",
        "   • Keep track of the best answer",
        "",
        "5. WHEN TO USE:",
        "   • Finding max/min of consecutive elements",
        "   • Finding averages of consecutive elements",
        "   • Finding subarrays/substrings with certain properties",
        "   • Any time you need to look at 'windows' of data",
    ]

    for concept in concepts:
        print(concept)

    print("=" * 60)


# ============================================================================
# RUN ALL EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("SLIDING WINDOW TECHNIQUE - Interactive Tutorial")
    print("=" * 60)

    # Example 1: Fixed window - Maximum sum
    example_1_the_slow_way()
    example_1_the_sliding_window_way()

    # Example 2: Fixed window - Temperature averages
    example_2_temperature_averages()

    # Example 3: Variable window - Find exact sum
    example_3_find_sum_variable_window()

    # Example 4: Variable window - Unique characters
    example_4_unique_characters()

    # Print summary
    print_key_concepts()

    print("\n✨ Now you understand sliding window! ✨")
    print("Try running this file and read through each example carefully!")
