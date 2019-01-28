package scanning;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.image.Image;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class Main extends Application {

    public static final int WIDTH = 500;            //  Значение ширины полотна
    public static final int HEIGHT = 500;           //  Значение высоты полотна
    public static final int INF = 1000000;          //  Значение неинициализации
    public static final int Z = -100000;            //  Начальное значение ячейки z-буфера
    public static final int BACKGROUND = 0;         //  Значение фона полотна

    @Override
    public void start(Stage primaryStage) throws Exception {
        Parent root = FXMLLoader.load(getClass().getResource("scene.fxml"));

        Scene scene = new Scene(root, WIDTH, HEIGHT);
        scene.setFill(Color.WHEAT);

        primaryStage.setTitle("Удаление невидимых граней");
        primaryStage.setResizable(false);
        primaryStage.setScene(scene);
        primaryStage.getIcons().add(new Image("/data/cube.png"));
        primaryStage.show();
    }


    /*
     *  Чтение данных из файла
     *  @return polygons: прочитанные из файла многоугольники
     *  @throws IOException: исключение ввода/вывода
     */
    public static ArrayList <Polygon> readingData() throws IOException {
        ArrayList <Polygon> polygons = new ArrayList<>();
        ArrayList <Point> points = new ArrayList<>();
        String[] line;

        BufferedReader fileReader = new BufferedReader(new FileReader(new File("src\\data\\input.txt")
                .getAbsolutePath()));
        int polygonCount = Integer.parseInt(fileReader.readLine());

        for (int i = 0; i < polygonCount; i++) {

            int pointCount = Integer.parseInt(fileReader.readLine());

            for (int j = 0; j < pointCount; j++) {
                line = fileReader.readLine().split("\\s");
                points.add(new Point(Integer.parseInt(line[0]), Integer.parseInt(line[1]),
                        Integer.parseInt(line[2])));
            }

            line = fileReader.readLine().split("\\s");
            polygons.add(new Polygon());
            polygons.get(i).addPolygon(points);
            polygons.get(i).setPolygonNumber(i + 1);
            polygons.get(i).setColor(Color.rgb(Integer.parseInt(line[0]), Integer.parseInt(line[1]),
                    Integer.parseInt(line[2])));
            points.clear();

        }

        return polygons;

    }

    /*
     *	Построчное сканирование с использованием z-буфера
     *	@param polygons: многоугольники
     *	@param canvas: полотно, где будут изображены многоугольники
     */
    public static void lineScanning(ArrayList<Polygon> polygons, Canvas canvas) {
        int[] zBuffer = new int[WIDTH];
        int[] screenBuffer = new int[WIDTH];


        ArrayList <Polygon> activePolygons = new ArrayList<>();
        ArrayList <Color> colors = new ArrayList<>();

        for (Polygon polygon : polygons) {
            colors.add(polygon.getColor());
        }

        //	Построчное сканирование по всем сканирующим строкам
        for (int y = 0; y < HEIGHT; y++) {

            //	Инициализация буферов
            initBuffer(zBuffer, Z);
            initBuffer(screenBuffer, BACKGROUND);

            /*
             *	Добавление активного многоугольника
             *  Если минимальное значение координаты y многоугольника
             *	Совпадает с текущей сканирующей строкой - заносим многоугольник в список активных
             */
            for (Polygon polygon : polygons) {

                if (polygon.getMinY() == y) {
                    activePolygons.add(polygon);
                }

            }

            //	Проверка активных рёбер многоугольников
            for (Polygon activePolygon : activePolygons) {
                activePolygon.checkingActiveEdges(y);
            }

            for (Polygon activePolygon : activePolygons) {
                //	Получаем пару рёбер текущего активного многоугольника
                Edge leftEdge = activePolygon.getLeftEdge();
                Edge rightEdge = activePolygon.getRightEdge();

                //	Для данной пары устанавливаем значение x + deltaX
                leftEdge.calculationExtensionX();
                rightEdge.calculationExtensionX();

                //	Получаем значение пересечения пары рёбер с текущей сканирующей строкой
                int xLeft = leftEdge.getExtensionX();
                int xRight = rightEdge.getExtensionX();

                if (xLeft > xRight) {
                    int storage = xLeft;
                    xLeft = xRight;
                    xRight = storage;

                    activePolygon.setLeftEdge(rightEdge);
                    activePolygon.setRightEdge(leftEdge);
                }

                //  Глубина
                double z = -(activePolygon.getA() * xLeft + activePolygon.getB() * y + activePolygon.getD()) /
                        activePolygon.getC();

                int x = xLeft;

                /*
                 *  Сравниваем глубину z(x, y) со значением в z-буфере в этой же позиции
                 *	Если z(x, y) больше, чем значение в z-буфере - записываем номер данного многоугольника в буфер экрана
                 *	В Z-буфер записываем значение глубины z(x, y);
                 *	Иначе - никаких действий не производим
                 */
                do {

                    if (z > zBuffer[x]) {

                        zBuffer[x] = (int)(z);
                        screenBuffer[x] = activePolygon.getPolygonNumber();

                    }

                    z -= (activePolygon.getA() / activePolygon.getC());
                    x++;

                } while (x <= xRight);

            }

            for (int i = 0; i < activePolygons.size(); i++) {
                int deltaY = activePolygons.get(i).getDeltaY();
                deltaY--;
                activePolygons.get(i).setDeltaY(deltaY);

                if (activePolygons.get(i).getDeltaY() == 0) {
                    activePolygons.remove(activePolygons.get(i));
                    i--;
                }

            }

            //	Наносим многоугольники на полотно
            for (int i = 0; i < WIDTH; i++) {

                if (screenBuffer[i] != 0) {
                    canvas.getGraphicsContext2D().getPixelWriter().setColor(i, y, colors.get(screenBuffer[i] - 1));
                }

            }

        }

    }

    /*
     *  Инициализация буфера
     *  @param buffer: непосредственно буфер
     *  @param value: значение инициализации
     */
    private static void initBuffer(int[] buffer, int value) {
        for (int i = 0; i < WIDTH; i++) {
            buffer[i] = value;
        }
    }


    public static void main(String[] args) {
        launch(args);
    }

}