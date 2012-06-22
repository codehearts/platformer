from settings import stageevents_library

class StageEvents(object):
    
    def __init__(self, player, camera, events):
        self.player = player
        self.camera = camera
        
        self.game_modules = {
            'player': self.player,
            'camera': self.camera
        }
        
        self.player_events = events['player_events']
    
    def check_player_event(self, event):
        # If the condition was met, run the event code
        if event['condition'](self.player):
            getattr(stageevents_library, event['function'])(self.game_modules)
            
            # If this function was supposed to run only once, don't keep it
            if event['run'] == 'once':
                return False
        
        return True
    
    def update(self):
        # Check for player events that need to fire
        self.player_events[:] = [x for x in self.player_events if self.check_player_event(x)] # Keep the original list reference