import tkinter as tk
from tkinter import messagebox
import random
import math
import threading
import time
class DataConnectorGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Data Connector")
        self.root.geometry("520x580")
        self.root.configure(bg='#0066cc')
        
        # Game states
        self.current_state = "title"  # "title" or "game"
        
        # Music settings
        self.music_enabled = True
        self.current_music_thread = None
        self.music_stop_flag = False
        
        # Game settings
        self.size = 6
        self.block_size = 70
        self.gap = 5
        
        # Circuit piece types (connections in 4 directions: North, East, South, West)
        self.piece_types = {
            'straight_h': [False, True, False, True],    # Horizontal line
            'straight_v': [True, False, True, False],    # Vertical line
            'corner_ne': [True, True, False, False],     # Corner North-East
            'corner_se': [False, True, True, False],     # Corner South-East
            'corner_sw': [False, False, True, True],     # Corner South-West
            'corner_nw': [True, False, False, True],     # Corner North-West
            'cross': [True, True, True, True],           # Cross (all directions)
            't_shape_n': [True, True, False, True],      # T-shape with top
            't_shape_e': [True, True, True, False],      # T-shape with right
            't_shape_s': [False, True, True, True],      # T-shape with bottom
            't_shape_w': [True, False, True, True],      # T-shape with left
        }
        
        # Initialize game variables
        self.board = []
        self.rotations = []
        self.packet_pos = None
        self.packet_path = []
        self.animation_id = None
        self.packet_index = 0
        
        self.show_title_screen()
        
    def show_title_screen(self):
        """Show the title screen"""
        self.current_state = "title"
        self.clear_screen()
        self.root.configure(bg='#0066cc')
        
        # Start title screen music
        self.play_title_music()
        
        # Main title frame
        title_frame = tk.Frame(self.root, bg='#0066cc')
        title_frame.pack(expand=True, fill='both')
        
        # Spacer
        tk.Frame(title_frame, bg='#0066cc', height=50).pack()
        
        # "DATA" text with Rocket Ranger style
        data_label = tk.Label(title_frame, text="DATA", 
                             font=("Impact", 48, "bold"), 
                             fg='#ff0000', bg='#0066cc',
                             relief='raised', bd=3)
        data_label.pack(pady=10)
        
        # "CONNECTOR" text with Rocket Ranger style
        connector_label = tk.Label(title_frame, text="CONNECTOR", 
                                  font=("Impact", 48, "bold"), 
                                  fg='#ff0000', bg='#0066cc',
                                  relief='raised', bd=3)
        connector_label.pack(pady=10)
        
        # Subtitle
        subtitle = tk.Label(title_frame, text="Circuit Connection Puzzle", 
                           font=("Arial", 14, "bold"), 
                           fg='#ffffff', bg='#0066cc')
        subtitle.pack(pady=20)
        
        # Button frame
        button_frame = tk.Frame(title_frame, bg='#0066cc')
        button_frame.pack(pady=30)
        
        # Start button
        start_btn = tk.Button(button_frame, text="START GAME", 
                             command=self.start_game,
                             font=("Arial", 16, "bold"),
                             bg='#ff0000', fg='white',
                             padx=30, pady=10,
                             relief='raised', bd=4)
        start_btn.pack(pady=10)
        
        # Music toggle button
        music_text = "MUSIC: ON" if self.music_enabled else "MUSIC: OFF"
        self.music_btn = tk.Button(button_frame, text=music_text, 
                                  command=self.toggle_music,
                                  font=("Arial", 12, "bold"),
                                  bg='#ffffff', fg='#0066cc',
                                  padx=20, pady=5,
                                  relief='raised', bd=3)
        self.music_btn.pack(pady=5)
        
        # Instructions
        instructions = tk.Label(title_frame, 
                               text="Connect circuits from IN to OUT\nRight-click blocks to rotate", 
                               font=("Arial", 11), 
                               fg='#cccccc', bg='#0066cc',
                               justify='center')
        instructions.pack(pady=20)
        
    def start_game(self):
        """Start the main game"""
        self.current_state = "game"
        self.stop_music()
        self.clear_screen()
        self.root.configure(bg='#1a1a2e')
        self.create_game_widgets()
        self.generate_puzzle()
        self.update_display()
        self.play_game_music()
        
    def clear_screen(self):
        """Clear all widgets from the screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def toggle_music(self):
        """Toggle music on/off"""
        self.music_enabled = not self.music_enabled
        music_text = "MUSIC: ON" if self.music_enabled else "MUSIC: OFF"
        
        if hasattr(self, 'music_btn'):
            self.music_btn.config(text=music_text)
            
        if not self.music_enabled:
            self.stop_music()
        else:
            if self.current_state == "title":
                self.play_title_music()
            elif self.current_state == "game":
                self.play_game_music()
                
    def play_title_music(self):
        """Play title screen music (simulated with beeps)"""
        if not self.music_enabled:
            return
            
        self.stop_music()
        self.music_stop_flag = False
        self.current_music_thread = threading.Thread(target=self._title_music_loop)
        self.current_music_thread.daemon = True
        self.current_music_thread.start()
        
    def play_game_music(self):
        """Play in-game music (simulated with beeps)"""
        if not self.music_enabled:
            return
            
        self.stop_music()
        self.music_stop_flag = False
        self.current_music_thread = threading.Thread(target=self._game_music_loop)
        self.current_music_thread.daemon = True
        self.current_music_thread.start()
        
    def stop_music(self):
        """Stop current music"""
        self.music_stop_flag = True
        if self.current_music_thread and self.current_music_thread.is_alive():
            self.current_music_thread.join(timeout=0.1)
            
    def _title_music_loop(self):
        """Title screen music loop - heroic/epic theme"""
        # Heroic chord progression (simulated with system beeps)
        title_melody = [800, 1000, 1200, 1000, 800, 600, 800, 1000]
        note_duration = 0.4
        
        while not self.music_stop_flag:
            for freq in title_melody:
                if self.music_stop_flag:
                    return
                try:
                    # Use a simple tone generation (cross-platform compatible)
                    self.root.bell()  # System bell as fallback
                    time.sleep(note_duration)
                except:
                    time.sleep(note_duration)
            time.sleep(1.0)  # Pause between loops
            
    def _game_music_loop(self):
        """Game music loop - electronic/tech theme"""
        # Electronic beat pattern
        game_melody = [400, 450, 500, 450, 400, 350, 400, 500]
        note_duration = 0.3
        
        while not self.music_stop_flag:
            for freq in game_melody:
                if self.music_stop_flag:
                    return
                try:
                    self.root.bell()  # System bell as fallback
                    time.sleep(note_duration)
                except:
                    time.sleep(note_duration)
            time.sleep(0.8)  # Shorter pause for more electronic feel
        
    def create_game_widgets(self):
        """Create the game interface widgets"""
        # Back to title button
        back_btn = tk.Button(self.root, text="← TITLE", 
                            command=self.show_title_screen,
                            font=("Arial", 10, "bold"),
                            bg='#666666', fg='white',
                            padx=10, pady=2)
        back_btn.place(x=10, y=10)
        
        # Title
        title = tk.Label(self.root, text="DATA CONNECTOR", 
                        font=("Impact", 18, "bold"), 
                        bg='#1a1a2e', fg='#00ff88')
        title.pack(pady=10)
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="Right-click blocks to rotate • Connect left to right for data flow", 
                               font=("Arial", 10), 
                               bg='#1a1a2e', fg='#888888')
        instructions.pack(pady=5)
        
        # Game frame
        self.game_frame = tk.Frame(self.root, bg='#16213e', bd=2, relief='raised')
        self.game_frame.pack(padx=20, pady=10)
        
        # Create canvas for the puzzle
        canvas_size = self.size * (self.block_size + self.gap) - self.gap
        self.canvas = tk.Canvas(self.game_frame, 
                               width=canvas_size, 
                               height=canvas_size,
                               bg='#16213e', highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        
        # Bind events
        self.canvas.bind("<Button-3>", self.on_right_click)  # Right click to rotate
        self.canvas.bind("<Button-1>", self.on_left_click)   # Left click for selection
        
        # Control buttons
        button_frame = tk.Frame(self.root, bg='#1a1a2e')
        button_frame.pack(pady=10)
        
        test_btn = tk.Button(button_frame, text="Test Circuit", 
                            command=self.test_circuit,
                            font=("Arial", 12, "bold"),
                            bg='#0066cc', fg='white',
                            padx=20, pady=5)
        test_btn.pack(side=tk.LEFT, padx=5)
        
        new_btn = tk.Button(button_frame, text="New Puzzle", 
                           command=self.generate_puzzle,
                           font=("Arial", 12, "bold"),
                           bg='#cc6600', fg='white',
                           padx=20, pady=5)
        new_btn.pack(side=tk.LEFT, padx=5)
        
        # Music toggle in game
        music_text = "♪ ON" if self.music_enabled else "♪ OFF"
        music_btn = tk.Button(button_frame, text=music_text, 
                             command=self.toggle_music,
                             font=("Arial", 10, "bold"),
                             bg='#444444', fg='white',
                             padx=15, pady=5)
        music_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Right-click blocks to rotate them", 
                                    font=("Arial", 11), 
                                    bg='#1a1a2e', fg='#00ff88')
        self.status_label.pack(pady=5)
        
    def generate_puzzle(self):
        """Generate a new puzzle with random pieces"""
        self.board = []
        self.rotations = []
        
        piece_names = list(self.piece_types.keys())
        
        for i in range(self.size):
            row = []
            rot_row = []
            for j in range(self.size):
                # Choose random piece type
                piece_type = random.choice(piece_names)
                row.append(piece_type)
                # Random initial rotation
                rot_row.append(random.randint(0, 3))
            self.board.append(row)
            self.rotations.append(rot_row)
        
        # Ensure there are entry and exit points
        # Left side entry (middle row)
        entry_row = self.size // 2
        self.board[entry_row][0] = 'straight_h'
        self.rotations[entry_row][0] = 0
        
        # Right side exit (middle row)
        exit_row = self.size // 2
        self.board[exit_row][self.size-1] = 'straight_h'
        self.rotations[exit_row][self.size-1] = 0
        
        if hasattr(self, 'canvas'):
            self.update_display()
        
    def draw_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        """Draw a rounded rectangle on the canvas"""
        points = []
        for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                     (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                     (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                     (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
            points.extend([x, y])
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
    def get_rotated_connections(self, piece_type, rotation):
        """Get the connections for a piece after rotation"""
        connections = self.piece_types[piece_type].copy()
        # Rotate connections (each rotation is 90 degrees clockwise)
        for _ in range(rotation):
            connections = [connections[3]] + connections[:-1]
        return connections
    
    def draw_circuit_piece(self, x, y, piece_type, rotation, highlight=False):
        """Draw a circuit piece with connections"""
        center_x = x + self.block_size // 2
        center_y = y + self.block_size // 2
        
        # Draw block background
        block_color = '#95a5a6' if not highlight else '#b8c5c8'
        self.draw_rounded_rect(x, y, x + self.block_size, y + self.block_size, 
                              radius=12, fill=block_color, outline='#7f8c8d', width=2)
        
        # Get rotated connections
        connections = self.get_rotated_connections(piece_type, rotation)
        
        # Draw connection lines
        line_width = 4
        connection_color = '#2c3e50'
        
        # Connection points (North, East, South, West)
        points = [
            (center_x, y + 10),           # North
            (x + self.block_size - 10, center_y),  # East
            (center_x, y + self.block_size - 10),  # South
            (x + 10, center_y)            # West
        ]
        
        # Draw connections based on piece type
        if piece_type == 'straight_h':
            if connections[1] and connections[3]:  # East-West
                self.canvas.create_line(points[3][0], points[3][1], 
                                      points[1][0], points[1][1], 
                                      width=line_width, fill=connection_color)
        elif piece_type == 'straight_v':
            if connections[0] and connections[2]:  # North-South
                self.canvas.create_line(points[0][0], points[0][1], 
                                      points[2][0], points[2][1], 
                                      width=line_width, fill=connection_color)
        elif 'corner' in piece_type:
            # Draw corner connections
            active_dirs = [i for i, conn in enumerate(connections) if conn]
            if len(active_dirs) == 2:
                # Draw lines from center to each active direction
                for direction in active_dirs:
                    self.canvas.create_line(center_x, center_y, 
                                          points[direction][0], points[direction][1], 
                                          width=line_width, fill=connection_color)
        elif piece_type == 'cross':
            # Draw cross (all four directions)
            for i, conn in enumerate(connections):
                if conn:
                    self.canvas.create_line(center_x, center_y, 
                                          points[i][0], points[i][1], 
                                          width=line_width, fill=connection_color)
        elif 't_shape' in piece_type:
            # Draw T-shape connections
            for i, conn in enumerate(connections):
                if conn:
                    self.canvas.create_line(center_x, center_y, 
                                          points[i][0], points[i][1], 
                                          width=line_width, fill=connection_color)
        
        # Draw center dot
        self.canvas.create_oval(center_x - 3, center_y - 3, 
                               center_x + 3, center_y + 3, 
                               fill=connection_color, outline=connection_color)
    
    def update_display(self):
        """Update the visual display of the puzzle"""
        if not hasattr(self, 'canvas'):
            return
            
        self.canvas.delete("all")
        
        for i in range(self.size):
            for j in range(self.size):
                x1 = j * (self.block_size + self.gap)
                y1 = i * (self.block_size + self.gap)
                
                piece_type = self.board[i][j]
                rotation = self.rotations[i][j]
                
                self.draw_circuit_piece(x1, y1, piece_type, rotation)
        
        # Draw entry and exit indicators
        entry_y = (self.size // 2) * (self.block_size + self.gap) + self.block_size // 2
        self.canvas.create_text(-15, entry_y, text="IN", 
                               font=("Arial", 12, "bold"), fill='#00ff88')
        
        canvas_width = self.size * (self.block_size + self.gap) - self.gap
        exit_y = (self.size // 2) * (self.block_size + self.gap) + self.block_size // 2
        self.canvas.create_text(canvas_width + 15, exit_y, text="OUT", 
                               font=("Arial", 12, "bold"), fill='#ff6666')
    
    def on_right_click(self, event):
        """Handle right clicks to rotate pieces"""
        col = event.x // (self.block_size + self.gap)
        row = event.y // (self.block_size + self.gap)
        
        if 0 <= row < self.size and 0 <= col < self.size:
            # Rotate the piece 90 degrees clockwise
            self.rotations[row][col] = (self.rotations[row][col] + 1) % 4
            self.update_display()
            if hasattr(self, 'status_label'):
                self.status_label.config(text=f"Rotated piece at ({row+1}, {col+1})")
    
    def on_left_click(self, event):
        """Handle left clicks for selection (future feature)"""
        pass
    
    def find_path(self):
        """Find if there's a complete path from left entry to right exit"""
        entry_row = self.size // 2
        entry_col = 0
        exit_row = self.size // 2
        exit_col = self.size - 1
        
        # BFS to find path
        from collections import deque
        queue = deque([(entry_row, entry_col, 1)])  # Start moving east from entry
        visited = set()
        path = {}
        
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # N, E, S, W
        
        while queue:
            row, col, from_dir = queue.popleft()
            
            if (row, col, from_dir) in visited:
                continue
            visited.add((row, col, from_dir))
            
            if row == exit_row and col == exit_col:
                # Found path to exit, reconstruct it
                result_path = []
                current = (row, col)
                while current in path:
                    result_path.append(current)
                    current = path[current]
                result_path.append((entry_row, entry_col))
                return list(reversed(result_path))
            
            # Check if current piece accepts connection from the direction we came from
            piece_type = self.board[row][col]
            rotation = self.rotations[row][col]
            connections = self.get_rotated_connections(piece_type, rotation)
            
            # Direction we came from (opposite of from_dir)
            came_from_dir = (from_dir + 2) % 4
            
            if not connections[came_from_dir]:
                continue  # This piece doesn't accept connection from where we came
            
            # Try all possible exits from this piece
            for exit_dir in range(4):
                if exit_dir != came_from_dir and connections[exit_dir]:
                    # Can exit in this direction
                    dr, dc = directions[exit_dir]
                    new_row, new_col = row + dr, col + dc
                    
                    if 0 <= new_row < self.size and 0 <= new_col < self.size:
                        if (new_row, new_col) not in path:
                            path[(new_row, new_col)] = (row, col)
                        queue.append((new_row, new_col, exit_dir))
        
        return None  # No path found
    
    def test_circuit(self):
        """Test if the circuit is complete and animate data flow"""
        path = self.find_path()
        
        if path:
            if hasattr(self, 'status_label'):
                self.status_label.config(text="Circuit complete! Data flowing...", fg='#00ff88')
            self.animate_data_packet(path)
        else:
            if hasattr(self, 'status_label'):
                self.status_label.config(text="Circuit incomplete! Rotate pieces to connect.", fg='#ff6666')
            messagebox.showinfo("Circuit Test", "Circuit is not complete!\nRotate pieces to create a path from IN to OUT.")
    
    def animate_data_packet(self, path):
        """Animate a data packet traveling through the circuit"""
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
        
        self.packet_path = path
        self.packet_index = 0
        self.draw_packet()
    
    def draw_packet(self):
        """Draw the data packet at current position"""
        if self.packet_index < len(self.packet_path):
            # Remove previous packet
            if hasattr(self, 'packet_id'):
                self.canvas.delete(self.packet_id)
            
            # Draw packet at current position
            row, col = self.packet_path[self.packet_index]
            x = col * (self.block_size + self.gap) + self.block_size // 2
            y = row * (self.block_size + self.gap) + self.block_size // 2
            
            self.packet_id = self.canvas.create_oval(x - 8, y - 8, x + 8, y + 8,
                                                    fill='#00ff88', outline='#ffffff', width=2)
            
            self.packet_index += 1
            self.animation_id = self.root.after(300, self.draw_packet)
        else:
            # Animation complete
            if hasattr(self, 'status_label'):
                self.status_label.config(text="Data packet delivered successfully!", fg='#00ff88')
            if hasattr(self, 'packet_id'):
                self.root.after(1000, lambda: self.canvas.delete(self.packet_id))
    
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        """Handle application closing"""
        self.stop_music()
        self.root.destroy()

if __name__ == "__main__":
    game = DataConnectorGame()
    game.run()
