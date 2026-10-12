import core.Environment as E
import core.Paramecium as P


def main():
    environment = E.Environment()
    paramecium = P.Paramecium(environment, p_num = 10)

    def setup(_environment: E.Environment):
        environment.generate_food()
        paramecium.generate_paramecium()


    def loop(_environment: E.Environment):
        environment.spread()
        paramecium.move_randomly()
        paramecium.sense_value()
        paramecium()

    def special(click_y,click_x):
        paramecium.update_click(click_y,click_x)

    E.start(environment, setup, loop, special, fps = 60)

if __name__ == '__main__':
    main()
