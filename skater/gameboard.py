
class GameBoard:
    # infinities to avoid crashes on empty sequence computations
    MIN_POSITION = -2 ** 31
    MAX_POSITION = 2 ** 31

    def __init__(self, obstacles):
        self.obstacles = obstacles

    def obstacles_under(self, player):
        """
        All the obstacles currently positioned under the player
        """
        ans = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.is_under(player.rect)]
        return ans


    def obstacles_right(self, player):
        """
        All the obstacles the player collides with to his right hand side
        """
        ans = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.is_to_the_right(player.rect)]  # the player's right border is the obstacle's left -> check obstacle's left collision
        return ans


    def obstacles_left(self, player):
        """
        All the obstacles the player collides with to his left hand side
        """
        ans = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.is_to_the_left(player.rect)]  # see `obstacles_right`
        return ans

    def limit_under(self, player):
        distances = [
            player.rect.distance_y(obstacle.rect)
            for obstacle in self.obstacles_under(player)]
        
        return min(distances + [self.MAX_POSITION])

    def limit_right(self, player):
        distances = [
            player.rect.distance_x(obstacle.rect)
            for obstacle in self.obstacles_right(player)]
        
        return min(distances + [self.MAX_POSITION])

    def limit_left(self, player):
        distances = [
            player.rect.distance_x(obstacle.rect)
            for obstacle in self.obstacles_left(player)]

        return max(distances + [self.MIN_POSITION])
