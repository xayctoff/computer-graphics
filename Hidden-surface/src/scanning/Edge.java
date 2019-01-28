package scanning;

import static scanning.Main.INF;

/*
 *  Класс, описывающий ребро многоугольника
 */
public class Edge {

    private double deltaX;              //  Приращение к значению координаты x
    private double overflow = 0;        //  Превышение приращения
    private int extensionX = INF;       //  Расширенное значение координаты x (старое значение + приращение)
    private Point start;                //  Начальная точка ребра
    private Point finish;               //  Конечная точка ребра


    /*
     *  Конструктор ребра без параметров
     */
    public Edge() {
        this.start = new Point();
        this.finish = new Point();
    }


    /*
     *	Конструктор ребра с параметрами для инициализации рёбер
     *	@param first: первый вектор с координатами точки
     *	@param second: второй вектор с координатами точки
     */
    public Edge(Point start, Point finish) {
        this.start = start;
        this.finish = finish;

        calculationDeltaX();
    }


    /*
     *  Расчёт приращения значения x
     */
    public void calculationDeltaX() {
        if (finish.getY() - start.getY() == 0) {
            deltaX = INF;
        }

        else {
            deltaX = ((double)(finish.getX() - start.getX())) / ((double)(finish.getY() - start.getY()));
        }

    }


    /*
     *  Расчёт нового значения координаты x с учётом старого значения и с учётом приращения
     */
    public void calculationExtensionX() {
        //  Если расширенное значение не инициализировано
        //  Сравним значения координаты y текущего ребра
        //  В зависимости от сравнения присваиваем значение координаты x расширенному значению
        //  Предполагается, что приращение нулевое
        if (extensionX == INF) {

            if (finish.getY() < start.getY()) {
                extensionX = finish.getX();
            }

            else {
                extensionX = start.getX();
            }

        }

        //  В противном случае, имеющееся приращение прибавляем к текущему значению превышения приращения
        else {
            overflow += deltaX;

            //  Если по модулю превышение больше или равно 1 - превышение обнуляется
            //  Текущее значение приращения прибавляем к расширенному значению координаты x
            if (Math.abs(overflow) >= 1) {
                overflow = 0;
                extensionX += deltaX;
            }

        }

    }


    /*
     *	Получить приращение координаты x
     *	@return deltaX: непосредственно приращение
     */
    public double getDeltaX() {
        return deltaX;
    }


    /*
     *	Получить расширенное значение координаты x
     *	@return extensionX: непосредственно значение
     */
    public int getExtensionX() {
        return extensionX;
    }


    /*
     *	Получить начальную точку ребра
     *	@return start: непосредственно начальная точка
     */
    public Point getStart() {
        return start;
    }


    /*
     *	Получить конечную точку ребра
     *	@return start: непосредственно конечная точка
     */
    public Point getFinish() {
        return finish;
    }

}