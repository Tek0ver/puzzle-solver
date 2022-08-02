import pygame


class UI:
    def __init__(self,display_surface, topleft):

        self.display_surface = display_surface
        self.topleft = topleft
        
        # text
        self.text_size = 30
        self.font = pygame.font.Font(None, self.text_size)

    def display_text(self, text, pos):

        text_surf = self.font.render(text, True, 'black')
        text_rect = text_surf.get_rect(topleft = pos)
        self.display_surface.blit(text_surf, text_rect)


    def display_moves_count(self, move_count, pos):

        text = f"Moves : {move_count}"
        self.display_text(text, pos)

    def display_animation_mode(self, animation, pos):
        
        if animation:
            animation = "ON"
        else:
            animation = "OFF"
            
        text = f"Animation mode : {animation}"
        self.display_text(text, pos)

    def run(self, move_count, animation):
        
        x = self.topleft
        y = 0

        for option, value in zip(
            [self.display_moves_count, self.display_animation_mode],
            [move_count, animation]):

            option(value, (x,y))
            y += self.text_size / 3 * 2
