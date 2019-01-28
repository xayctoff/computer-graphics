package scanning;

/*
 *  Класс, описывающий точку многоугольника
 */
public class Point {

    //  Координаты точки
    private int x;
    private int y;
    private int z;


    /*
     *  Конструктор точки без параметров
     */
    public Point() {}


    /*
     *	Конструктор точки с параметрами
     *	@param x: координата x
     *	@param y: координата y
     *	@param z: координата z
     */
    public Point(int x, int y, int z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }


    /*
     *	Получить координату x
     *	@return x: непосредственно координата
     */
    public int getX() {
        return x;
    }

    /*
     *	Получить координату y
     *	@return y: непосредственно координата
     */
    public int getY() {
        return y;
    }

    /*
     *	Получить координату z
     *	@return z: непосредственно координата
     */
    public int getZ() {
        return z;
    }

}