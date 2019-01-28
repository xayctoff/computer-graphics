package scanning;

import javafx.scene.paint.Color;
import java.util.ArrayList;

import static scanning.Main.INF;

/*
 *  Класс, описывающий непосредственно многоугольник
 */
public class Polygon {

    //  Коэффициенты уравнения плоскости
    private double a;
    private double b;
    private double c;
    private double d;

    private int minY;               //  Минимальное значение координаты y
    private int deltaY;             //  Разница между минимальным и максимальным значением координаты y
    private int polygonNumber;      //  Номер многоугольника

    private Color color;            //  Цвет многоугольника

    private ArrayList <Point> points = new ArrayList<>();       //  Точки многоугольника
    private ArrayList <Edge> edges = new ArrayList<>();         //  Рёбра многоугольника

    private Edge leftEdge = new Edge();                         //  Левое активное ребро
    private Edge rightEdge = new Edge();                        //  Правое активное ребро


    /*
     *  Добавление многоугольника с последующей инициализацией
     *  @param points: точки многоугольника
     */
    public void addPolygon(ArrayList <Point> points) {
        this.points.addAll(points);

        addEdges();
        calculationDeltaY();
        calculationCoefficients();
        calculationD();
    }

    /*
     *  Добавление рёбер
     */
    private void addEdges() {
        for (int i = 1; i < points.size(); i++) {

            Edge edge = new Edge(points.get(i - 1), points.get(i));
            edges.add(edge);

        }

        //	Добавление последнего ребра, замыкающего многоугольник
        edges.add(new Edge(points.get(points.size() - 1), points.get(0)));
    }

    /*
     *  Расчёт коэффициентов a, b, c уравнения плоскости
     */
    private void calculationCoefficients() {
        double a = 0;
        double b = 0;
        double c = 0;

        for (int i = 0, j = 1; i < points.size(); i++, j++) {

            if (i == points.size() - 1) {
                j = 0;
            }

            a += (points.get(i).getY() - points.get(j).getY()) * (points.get(i).getZ() + points.get(j).getZ());
            b += (points.get(i).getZ() - points.get(j).getZ()) * (points.get(i).getX() + points.get(j).getX());
            c += (points.get(i).getX() - points.get(j).getX()) * (points.get(i).getY() + points.get(j).getY());

        }

        this.a = a;
        this.b = b;
        this.c = c;
    }

    /*
     *  Расчёт коэффициента d уравнения плоскости
     */
    private void calculationD() {
        d = -(a * points.get(0).getX() + b * points.get(0).getY() + c * points.get(0).getZ());
    }

    /*
     *  Расчёт значения разницы между максимальным и минимальным значением координаты y
     */
    private void calculationDeltaY() {
        int min = INF;
        int max = -INF;

        for (Point point : points) {

            int y = point.getY();

            if (y < min) {
                min = y;
            }

            if (y > max) {
                max = y;
            }

        }

        deltaY = max - min;
        minY = min;
    }

    /*
     *	Проверка активных рёбер многоугольника
     *	@param line: сканирующая строка
     */
    public void checkingActiveEdges(int line) {
        Edge leftEdge = getLeftEdge();
        Edge rightEdge = getRightEdge();

        rightEdge = checkingConcreteActiveEdge(rightEdge, line);
        leftEdge = checkingConcreteActiveEdge(leftEdge, line);

        if (leftEdge.getExtensionX() > rightEdge.getExtensionX()) {
            setLeftEdge(rightEdge);
            setRightEdge(leftEdge);
        }

        else {
            setLeftEdge(leftEdge);
            setRightEdge(rightEdge);
        }

    }

    /*
     *  Проверка конкретного активного ребра
     *  @param activeEdge: непосредственно ребро
     *  @param line: сканирующая строка
     *  @return activeEdge: модифицированное активное ребро
     */
    private Edge checkingConcreteActiveEdge(Edge activeEdge, int line) {
        //	Проверяем, если сканирующая строка входит в диапазон значений координаты y начальной и конечной точки правого ребра
        if (!((activeEdge.getStart().getY() <= line && line <= activeEdge.getFinish().getY()) ||
              (activeEdge.getFinish().getY() <= line && line <= activeEdge.getStart().getY()))) {

            for (Edge edge : edges) {

                if (edge.getDeltaX() == INF) {
                    continue;
                }

                if ((edge.getStart().getY() == line - 1 && edge.getFinish().getY() > line) ||
                    (edge.getFinish().getY() == line - 1 && edge.getStart().getY() > line)) {

                    activeEdge = edge;
                    activeEdge.calculationExtensionX();
                    edges.remove(edge);
                    break;

                }

                if ((edge.getStart().getY() == line && edge.getFinish().getY() > line) ||
                    (edge.getFinish().getY() == line && edge.getStart().getY() > line)) {

                    activeEdge = edge;
                    edges.remove(edge);
                    break;

                }

            }

        }

        return activeEdge;
    }

    /*
     *  Получить коэффициент а
     *  @return a: непосредственно коэффициент
     */
    public double getA() {
        return a;
    }

    /*
     *  Получить коэффициент b
     *  @return b: непосредственно коэффициент
     */
    public double getB() {
        return b;
    }

    /*
     *  Получить коэффициент c
     *  @return c: непосредственно коэффициент
     */
    public double getC() {
        return c;
    }


    /*
     *  Получить коэффициент d
     *  @return d: непосредственно коэффициент
     */
    public double getD() {
        return d;
    }


    /*
     *  Получить минимальное значение координаты y
     *  @return minY: непосредственно значение
     */
    public int getMinY() {
        return minY;
    }


    /*
     *  Получить значение разницы между максимальным и минимальным значением координаты y
     *  @return deltaY: непосредственно значение
     */
    public int getDeltaY() {
        return deltaY;
    }


    /*
     *  Установить значение разницы между максимальным и минимальным значением координаты y
     *  @param deltaY: устанавливаемое значение
     */
    public void setDeltaY(int deltaY) {
        this.deltaY = deltaY;
    }


    /*
     *  Получить номер многоугольника
     *  @return polygonNumber: непосредственно номер
     */
    public int getPolygonNumber() {
        return polygonNumber;
    }


    /*
     *  Установить номер многоугольника
     *  @param polygonNumber: устанавливаемый номер
     */
    public void setPolygonNumber(int polygonNumber) {
        this.polygonNumber = polygonNumber;
    }


    /*
     *  Получить цвет многоугольника
     *  @return color: непосредственно цвет
     */
    public Color getColor() {
        return color;
    }


    /*
     *  Установить цвет многоугольника
     *  @param color: устанавливаемый цвет
     */
    public void setColor(Color color) {
        this.color = color;
    }


    /*
     *  Получить левое активное ребро
     *  @return leftEdge: непосредственно ребро
     */
    public Edge getLeftEdge() {
        return leftEdge;
    }

    /*
     *  Получить левое активное ребро
     *  @param leftEdge: устанавливаемое ребро
     */
    public void setLeftEdge(Edge leftEdge) {
        this.leftEdge = leftEdge;
    }


    /*
     *  Получить правое активное ребро
     *  @return rightEdge: непосредственно ребро
     */
    public Edge getRightEdge() {
        return rightEdge;
    }


    /*
     *  Установить правое активное ребро
     *  @param rightEdge: непосредственно ребро
     */
    public void setRightEdge(Edge rightEdge) {
        this.rightEdge = rightEdge;
    }

}