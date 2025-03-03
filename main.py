import pygame
import pygame_gui
import time
import math
from button import Button
from graphicnode import GraphicNode
from icons import *
import threading

nodes = []

connect_node = None
connecting_node = None
menu = None

running = True



def pygame_loop(): # Main Pygame Loop
    global running
    global menu
    global nodes
    global connect_node
    global connecting_node

    # Initialize Pygame
    pygame.init()

    # Screen dimensions (initial)
    WIDTH, HEIGHT = 800, 600

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Create a resizable window
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Peter's Control System")
    pygame.font.init()

    current_page = 1 # 0=Home, 1=Program, 2=IO

    def dist(xy1, xy2):
        return math.sqrt((xy2[0]-xy1[0])**2 + (xy2[1]-xy1[1])**2)

    def goHome():
        nonlocal current_page
        print(f"Current Page: {current_page}")
        current_page = 0

    def goProgram():
        nonlocal current_page
        print(f"Current Page: {current_page}")
        current_page = 1

    def kill_menu():
        global menu
        node_label_entry.visible=False
        node_type_label.visible=False
        node_label_label.visible=False
        node_duration_entry.visible=False
        node_duration_label.visible=False
        node_subtype_entry.visible=False
        node_subtype_entry.hide()
        node_subtype_entry.kill()
        node_subtype_entry.disable()
        node_subtype_label.visible=False
        menu = None

    barnodes = [GraphicNode(screen, 1, (255,5), bar=True), GraphicNode(screen, 2, (300,5), bar=True), GraphicNode(screen, 3, (345,5), bar=True), GraphicNode(screen, 4, (430,5), bar=True), GraphicNode(screen, 5, (475,5), bar=True)]

    home_button = Button(screen, "Home", pygame.Rect(0, 0, 100, 50), goHome)
    program_button = Button(screen, "Program", pygame.Rect(100, 0, 150, 50), goProgram)

    buttons=[home_button, program_button]

    old_screen_pos = (0,0)
    screen_pos = (0,0)

    cursor = pygame.SYSTEM_CURSOR_ARROW
    mousedown_time = 0
    new_node = None

    grab_page = False
    grab_node = False

    mousedown_pos = (0,0)
    mousedown = 0
    mouseRdown = 0
    ignore_mousedown = 0
    ignore_mouseRdown = 0

    MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT), 'theme.json')

    node_type_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 50), (200, 30)), text="", manager=MANAGER, object_id="#node_type_label", visible=False)
    node_label_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 50), (50, 30)), text="Label", manager=MANAGER, object_id="#node_label_label", visible=False)
    node_label_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 50), (150, 30)), manager=MANAGER, object_id="#node_label_entry", visible=False)

    node_duration_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 50), (100, 30)), text="Duration (sec)", manager=MANAGER, object_id="#node_duration_label", visible=False)
    node_duration_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((50, 50), (100, 30)), manager=MANAGER, object_id="#node_duration_entry", visible=False)

    node_subtype_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 50), (50, 30)), text="Type", manager=MANAGER, object_id="#node_subtype_label", visible=False)
    node_subtype_entry = pygame_gui.elements.UIDropDownMenu(options_list=[""], starting_option="", relative_rect=pygame.Rect((50, 50), (150, 30)), manager=MANAGER, object_id="#node_subtype_entry", visible=False)

    CLOCK = pygame.time.Clock()
    

    main_font = pygame.font.Font("font.ttf", 18)
    main_font.set_bold(True)

    while running:
        UI_REFRESH_RATE = CLOCK.tick(60)/1000

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE: #Handles window resize events.
                WIDTH, HEIGHT = event.size
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE) #Resize the screen.
                MANAGER.set_window_resolution((WIDTH, HEIGHT))
            MANAGER.process_events(event)
            if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if menu:
                    menu.label = node_label_entry.get_text()
                    if menu.type == 3:
                        try:
                            menu.duration = float(node_duration_entry.get_text())
                        except Exception:
                            pass
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if menu:
                    if menu.type == 3:
                        menu.timer_type = int(node_subtype_entry.selected_option[1])

        MANAGER.update(UI_REFRESH_RATE)
        
        cursor = pygame.SYSTEM_CURSOR_ARROW
        if current_page == 0:
            for node in nodes:
                if node.collidepoint(pygame.mouse.get_pos()) and (node.connection == None or node.type == 1):
                    if not node.bar:
                        cursor = pygame.SYSTEM_CURSOR_HAND
        pygame.mouse.set_cursor(cursor)           

        if pygame.mouse.get_pressed()[0]: # When the mouse left button is pressed
            if not (menu and menu_rect.collidepoint(pygame.mouse.get_pos())) or grab_page or grab_node:
                if not mousedown: # If it was not pressed before
                    if not pygame.Rect(0,0,WIDTH,50).collidepoint(pygame.mouse.get_pos()) and not ignore_mousedown: # If the mouse is not on the top bar and is not being ignored
                        if current_page == 1:
                            for node in nodes:
                                if node.collidepoint(pygame.mouse.get_pos()):
                                    print("Grabbed node")
                                    grab_node = node
                                    grab_node.old_pos = pygame.Rect(node.pos)
                            if not grab_node:
                                grab_page = True
                                old_screen_pos = screen_pos
                        if current_page == 0:
                            for node in nodes:
                                if node.collidepoint(pygame.mouse.get_pos()) and (node.connection == None or node.type == 1):
                                    print("Toggled node")
                                    node.value = not node.value
                        mousedown = 1
                        mousedown_pos = pygame.mouse.get_pos()
                        mousedown_location = pygame.mouse.get_pos()
                    else:
                        ignore_mousedown = 1
                        if current_page == 1:
                            for node in barnodes:
                                if node.collidepoint(pygame.mouse.get_pos()):
                                    grab_node = GraphicNode(screen, node.type, (pygame.mouse.get_pos()[0]+screen_pos[0], pygame.mouse.get_pos()[1]-screen_pos[1]+50))
                                    new_node = grab_node
                                    nodes.append(grab_node)
                                    ignore_mousedown = 0
                                    print("Grabbed new node")
                                    grab_node.old_pos = pygame.Rect(node.pos)
                                    mousedown = 1
                                    mousedown_pos = (pygame.mouse.get_pos()[0]+screen_pos[0], pygame.mouse.get_pos()[1]+screen_pos[1]+50)
                                    mousedown_location = pygame.mouse.get_pos()
                        
                else:
                    if grab_page:
                        screen_pos = (old_screen_pos[0] + (pygame.mouse.get_pos()[0] - mousedown_pos[0]), old_screen_pos[1] + (pygame.mouse.get_pos()[1] - mousedown_pos[1]))
                    if grab_node:
                        grab_node.pos = grab_node.old_pos.move(pygame.mouse.get_pos()[0] - mousedown_pos[0], pygame.mouse.get_pos()[1] - mousedown_pos[1])
            else:
                ignore_mousedown = 1
            if not mousedown:
                mousedown_location = pygame.mouse.get_pos()
                mousedown_time = time.time()
            mousedown = 1
        else:
            if not (menu and menu_rect.collidepoint(pygame.mouse.get_pos())):
                if mousedown:
                    if dist(mousedown_location, pygame.mouse.get_pos()) < 2: # If this was a click, not a click and drag
                        print("Click")
                        if menu:
                            kill_menu()
                        for node in nodes:
                                if node.collidepoint(pygame.mouse.get_pos()):
                                    if current_page == 1:
                                        if not node.bar:
                                            menu = node
                                            node_label_entry.set_text(menu.label)
                                            node_duration_entry.set_text(str(menu.duration))
                                            if node.type == 3:
                                                if node.timer_type == 0: # Delay
                                                    starting_option = ("Delay", "0")
                                                elif node.timer_type == 1: # On-Delay
                                                    starting_option = ("On-Delay", "1")
                                                elif node.timer_type == 2: # Off-Delay
                                                    starting_option = ("Off-Delay", "2")
                                                elif node.timer_type == 3: # Clock
                                                    starting_option = ("Clock", "3")
                                                node_subtype_entry = pygame_gui.elements.UIDropDownMenu(options_list=[("Delay", "0"), ("On-Delay", "1"), ("Off-Delay", "2"), ("Clock", "3")], starting_option=starting_option, relative_rect=pygame.Rect((50, 50), (150, 30)), manager=MANAGER, object_id="#node_subtype_entry", visible=False)
                                                    
                                        print(menu)
                        if new_node == grab_node:
                            print("New node was not moved, so deleted")
                            nodes.remove(grab_node)
                            grab_node.delete()
                            kill_menu()
                    else:
                        if grab_node:
                            if pygame.Rect(WIDTH-45, 5, 40, 40).collidepoint(pygame.mouse.get_pos()):
                                print("Deleted Node")
                                nodes.remove(grab_node)
                                grab_node.delete()
            mousedown = 0
            ignore_mousedown=0
            old_screen_pos = screen_pos
            grab_page = False
            grab_node = False
            new_node = None

        if pygame.mouse.get_pressed()[2]: # When the mouse right button is pressed
            if not mouseRdown:
                if not pygame.Rect(0,0,WIDTH,50).collidepoint(pygame.mouse.get_pos()) and not ignore_mouseRdown: # If the mouse is not on the top bar and is not being ignored
                    if current_page == 1: # Programming page
                        print("Trying to connect node")
                        for node in nodes:
                            if node.collidepoint(pygame.mouse.get_pos()) and (node.type!=1):
                                print("Connecting node")
                                connect_node = node
                                
                                if connect_node.type == 5:
                                    if node.in_1_rect.collidepoint(pygame.mouse.get_pos()):
                                        connect_node.connection = None
                                        connect_input = 1
                                    elif node.in_2_rect.collidepoint(pygame.mouse.get_pos()):
                                        connect_node.connection_2 = None
                                        connect_input = 2
                                    print(connect_input)
                                else:
                                    connect_node.connection = None
                    mouseRdown = 1
                    mouseRdown_pos = pygame.mouse.get_pos()
                else:
                    ignore_mousedown = 1
            else:
                if connect_node:
                    connecting_node = None
                    for node in nodes:
                        if node.collidepoint(pygame.mouse.get_pos()): # and (node.type == 1):
                            connecting_node = node
        else:
            mouseRdown = 0
            ignore_mouseRdown = 0
            if connect_node:
                if connecting_node:
                    if connect_node.type == 5:
                        if connect_input == 1:
                            connect_node.connection = connecting_node
                        elif connect_input == 2:
                            connect_node.connection_2 = connecting_node
                    else:
                        connect_node.connection = connecting_node
                    connecting_node = None
                connect_node = None



        for button in buttons:
            button.update(pygame.mouse)

        for node in nodes:
            node.update(screen_pos)
        
        for node in barnodes:
            node.update()
        
        if current_page == 0:
            home_button.set_color((80,100,255))
            program_button.set_color((128,128,128))
            menu = None
        elif current_page == 1:
            home_button.set_color((128,128,128))
            program_button.set_color((80,100,255))

        # Drawing
        screen.fill(WHITE)

        if connect_node:
            if connecting_node:
                if connect_node.type == 5:
                    if connect_input == 1:
                        pygame.draw.line(screen, (0,0, 0), connect_node.connect_in_point, connecting_node.connect_out_point, 3)
                    elif connect_input == 2:
                        pygame.draw.line(screen, (0,0, 0), connect_node.connect_in_point_2, connecting_node.connect_out_point, 3)
                else:
                    pygame.draw.line(screen, (0,0, 0), connect_node.connect_in_point, connecting_node.connect_out_point, 3)
            else:
                if connect_node.type == 5:
                    if connect_input == 1:
                        pygame.draw.line(screen, (0,0, 0), connect_node.connect_in_point, pygame.mouse.get_pos(), 3)
                    elif connect_input == 2:
                        pygame.draw.line(screen, (0,0, 0), connect_node.connect_in_point_2, pygame.mouse.get_pos(), 3)
                else:
                    pygame.draw.line(screen, (0,0, 0), connect_node.connect_in_point, pygame.mouse.get_pos(), 3)

        if current_page == 1:
            for node in nodes:
                node.draw_connection()
        for node in nodes:
            node.draw()

        # Draw Menu
        if menu:
            menu_rect = pygame.Rect(menu.rect.right+4, menu.rect.top, 200, 300)
            pygame.draw.rect(screen, (128,128,128), menu_rect)

            node_label_entry.set_position(pygame.Rect(menu_rect.left+50, menu_rect.top+30, menu_rect.width-50, 30))
            node_label_label.set_position(pygame.Rect(menu_rect.left, menu_rect.top+30, 50, 30))
            node_label_entry.visible=True
            node_label_label.visible=True

            node_type_label.set_position(pygame.Rect(menu_rect.left, menu_rect.top, menu_rect.width, 30))
            if menu.type == 1:
                node_type_label.set_text("Digital Input")
            if menu.type == 2:
                node_type_label.set_text("Digital Output")
            if menu.type == 3:
                node_type_label.set_text("Timer")
                node_duration_entry.set_position(pygame.Rect(menu_rect.left+100, menu_rect.top+60, menu_rect.width-100, 30))
                node_duration_label.set_position(pygame.Rect(menu_rect.left, menu_rect.top+60, 100, 30))
                node_duration_entry.visible=True
                node_duration_label.visible=True

                node_subtype_entry.set_position(pygame.Rect(menu_rect.left+50, menu_rect.top+90, menu_rect.width-150, 30))
                node_subtype_label.set_position(pygame.Rect(menu_rect.left, menu_rect.top+90, 50, 30))
                node_subtype_entry.visible=True
                node_subtype_label.visible=True
                node_subtype_entry.show()
                node_subtype_entry.enable()
            if menu.type == 4:
                node_type_label.set_text("Digital Inverter")
            if menu.type == 5:
                node_type_label.set_text("Digital Logic Gate")
            node_type_label.visible=True
        else:
            kill_menu()

        MANAGER.draw_ui(screen)

        if current_page == 1:
            for node in barnodes:
                node.draw()
            screen.blit(delete_icon, (WIDTH-45, 5))

        for button in buttons:
            button.draw()

        
        

        # Draw your objects here
        # pygame.draw.rect(screen, BLACK, (100, 100, 50, 50)) # Example

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

def processing_loop():
    global running
    while running:
    # Purge deleted nodes
        for node in nodes:
            if node.deleted:
                nodes.remove(node)
            if node.connection:
                if node.connection.deleted:
                    node.connection = None
            if node.connection_2:
                if node.connection_2.deleted:
                    node.connection_2 = None
            node.process()
            

    

pygame_thread = threading.Thread(target=pygame_loop)
processing_thread = threading.Thread(target=processing_loop)

pygame_thread.start()
processing_thread.start()
