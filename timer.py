
def run():
    import pygame
    import time
    import tkinter as tk
    from tkinter import ttk
    from ttkthemes import ThemedTk
    import threading

    # Initialize Pygame
    pygame.init()

    # Create the ModernTkinter window using ttkthemes
    root = ThemedTk(theme="arc")  # Modern Tkinter theme
    root.title("Timer/Stopwatch")
    root.geometry("600x600")

    # Set background color or image
    root.configure(bg='#2E2E2E')  # Dark background for a sleek look

    # Pygame window size and setup (Resizable window)
    screen_width = 600
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    # Timer variables
    start_time = 0
    elapsed_time = 0
    running = False
    countdown_time = 0  # For the countdown timer
    countdown_running = False  # To track the state of the countdown timer

    # Function to update the stopwatch
    def update_stopwatch():
        global elapsed_time
        global start_time
        global running
        font = pygame.font.Font(None, 40)

        while running:
            elapsed_time = time.time() - start_time
            # Clear the screen with a gradient
            screen.fill((0, 0, 0))

            # Convert elapsed time to hours, minutes, seconds, and milliseconds
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)
            milliseconds = int((elapsed_time * 1000) % 1000)

            # Render the stopwatch time
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}:{milliseconds:03}"

            # Render the time to the Pygame window
            time_surface = font.render(time_str, True, (255, 255, 255))
            screen_width, screen_height = pygame.display.get_window_size()
            screen.blit(time_surface, (screen_width // 2 - time_surface.get_width() // 2, screen_height // 2 - time_surface.get_height() // 2))

            pygame.display.flip()
            time.sleep(0.01)

    # Function to update the countdown timer
    def update_timer():
        global countdown_time
        global countdown_running
        font = pygame.font.Font(None, 40)

        while countdown_running and countdown_time > 0:
            countdown_time = max(0, countdown_time - 1)
            # Clear the screen with a gradient
            screen.fill((0, 0, 0))

            # Convert countdown time to hours, minutes, and seconds
            hours = countdown_time // 3600
            minutes = (countdown_time % 3600) // 60
            seconds = countdown_time % 60

            # Render the timer time
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"

            # Render the time to the Pygame window
            time_surface = font.render(time_str, True, (255, 255, 255))
            screen_width, screen_height = pygame.display.get_window_size()
            screen.blit(time_surface, (screen_width // 2 - time_surface.get_width() // 2, screen_height // 2 - time_surface.get_height() // 2))

            pygame.display.flip()
            time.sleep(1)

    # Function to start the stopwatch
    def start_stopwatch():
        global start_time
        global running
        start_time = time.time() - elapsed_time
        running = True
        threading.Thread(target=update_stopwatch, daemon=True).start()

    # Function to stop the stopwatch
    def stop_stopwatch():
        global running
        running = False

    # Function to reset the stopwatch
    def reset_stopwatch():
        global elapsed_time
        global running
        running = False
        elapsed_time = 0

    # Function to start the countdown timer
    def start_timer(hour, minute, second):
        global countdown_time
        global countdown_running

        countdown_time = hour * 3600 + minute * 60 + second  # Convert to total seconds
        countdown_running = True
        threading.Thread(target=update_timer, daemon=True).start()

    # Function to stop the countdown timer
    def stop_timer():
        global countdown_running
        countdown_running = False

    # Function to reset the countdown timer
    def reset_timer():
        global countdown_time
        global countdown_running
        countdown_running = False
        countdown_time = 0

    # Function to handle timer/stopwatch selection
    def switch_mode():
        global running, countdown_running

        selected_mode = mode_var.get()

        if selected_mode == "Stopwatch":
            stopwatch_frame.pack_forget()
            timer_frame.pack_forget()
            stopwatch_frame.pack(pady=20)
        elif selected_mode == "Timer":
            stopwatch_frame.pack_forget()
            timer_frame.pack_forget()
            timer_frame.pack(pady=20)

    # Function to create the stopwatch buttons with hover effect
    def create_stopwatch_buttons():
        def on_enter(e):
            e.widget.config(bg="#4CAF50")  # Hover effect (green)
        
        def on_leave(e):
            e.widget.config(bg="#3e8e41")  # Reset to original color
        
        # Start Button
        start_button = tk.Button(stopwatch_frame, text="Start", command=start_stopwatch, bg="#3e8e41", fg="white", font=('Helvetica', 12, 'bold'))
        start_button.pack(pady=10)
        start_button.bind("<Enter>", on_enter)
        start_button.bind("<Leave>", on_leave)

        # Stop Button
        stop_button = tk.Button(stopwatch_frame, text="Stop", command=stop_stopwatch, bg="#f44336", fg="white", font=('Helvetica', 12, 'bold'))
        stop_button.pack(pady=10)
        stop_button.bind("<Enter>", on_enter)
        stop_button.bind("<Leave>", on_leave)

        # Reset Button
        reset_button = tk.Button(stopwatch_frame, text="Reset", command=reset_stopwatch, bg="#FF9800", fg="white", font=('Helvetica', 12, 'bold'))
        reset_button.pack(pady=10)
        reset_button.bind("<Enter>", on_enter)
        reset_button.bind("<Leave>", on_leave)

    # Function to create the timer buttons with hover effect
    def create_timer_buttons():
        def on_enter(e):
            e.widget.config(bg="#4CAF50")  # Hover effect (green)
        
        def on_leave(e):
            e.widget.config(bg="#3e8e41")  # Reset to original color
        
        # Hour, Minute, Second input for countdown timer
        hour_label = tk.Label(timer_frame, text="Hours:", font=('Helvetica', 12))
        hour_label.pack(pady=5)
        hour_entry = tk.Entry(timer_frame, font=('Helvetica', 12))
        hour_entry.pack(pady=5)
        hour_entry.insert(0, "0")  # Default to 0 hours

        minute_label = tk.Label(timer_frame, text="Minutes:", font=('Helvetica', 12))
        minute_label.pack(pady=5)
        minute_entry = tk.Entry(timer_frame, font=('Helvetica', 12))
        minute_entry.pack(pady=5)
        minute_entry.insert(0, "1")  # Default to 1 minute

        second_label = tk.Label(timer_frame, text="Seconds:", font=('Helvetica', 12))
        second_label.pack(pady=5)
        second_entry = tk.Entry(timer_frame, font=('Helvetica', 12))
        second_entry.pack(pady=5)
        second_entry.insert(0, "0")  # Default to 0 seconds

        # Start Button
        start_button = tk.Button(timer_frame, text="Start Timer", command=lambda: start_timer(int(hour_entry.get()), int(minute_entry.get()), int(second_entry.get())), bg="#3e8e41", fg="white", font=('Helvetica', 12, 'bold'))
        start_button.pack(pady=10)
        start_button.bind("<Enter>", on_enter)
        start_button.bind("<Leave>", on_leave)

        # Stop Button
        stop_button = tk.Button(timer_frame, text="Stop Timer", command=stop_timer, bg="#f44336", fg="white", font=('Helvetica', 12, 'bold'))
        stop_button.pack(pady=10)
        stop_button.bind("<Enter>", on_enter)
        stop_button.bind("<Leave>", on_leave)

        # Reset Button
        reset_button = tk.Button(timer_frame, text="Reset Timer", command=reset_timer, bg="#FF9800", fg="white", font=('Helvetica', 12, 'bold'))
        reset_button.pack(pady=10)
        reset_button.bind("<Enter>", on_enter)
        reset_button.bind("<Leave>", on_leave)

    # Create radio buttons to select between Timer or Stopwatch
    mode_var = tk.StringVar(value="Stopwatch")
    mode_radio_frame = tk.Frame(root, bg='#2E2E2E')
    stopwatch_radio = tk.Radiobutton(mode_radio_frame, text="Stopwatch", variable=mode_var, value="Stopwatch", command=switch_mode, bg='#2E2E2E', fg="white", font=('Helvetica', 12))
    stopwatch_radio.pack(side="left", padx=10)
    timer_radio = tk.Radiobutton(mode_radio_frame, text="Timer", variable=mode_var, value="Timer", command=switch_mode, bg='#2E2E2E', fg="white", font=('Helvetica', 12))
    timer_radio.pack(side="left", padx=10)

    mode_radio_frame.pack(pady=20)

    # Create frames for stopwatch and timer
    stopwatch_frame = tk.Frame(root, bg='#2E2E2E')
    create_stopwatch_buttons()

    timer_frame = tk.Frame(root, bg='#2E2E2E')
    create_timer_buttons()

    # Switch to default mode
    switch_mode()

    # Start the Tkinter event loop
    root.mainloop()
run()