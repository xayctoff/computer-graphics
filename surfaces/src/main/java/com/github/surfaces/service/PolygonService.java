package com.github.surfaces.service;

import com.github.surfaces.model.Edge;
import com.github.surfaces.model.Point;
import com.github.surfaces.model.Polygon;

import java.util.ArrayList;
import java.util.List;

public class PolygonService {

    /**
     * Создание многоугольника
     *
     * @param points список точек
     */
    public Polygon createPolygon(List<Point> points) {
        Polygon polygon = new Polygon();
        polygon.setPoints(points);

        addEdges(polygon);
        calculateA(polygon);
        calculateB(polygon);
        calculateC(polygon);
        calculateD(polygon);

        return polygon;
    }

    /**
     * Добавление рёбер
     *
     * @param polygon непосредственно многоугольник
     */
    public void addEdges(Polygon polygon) {
        List<Point> points = polygon.getPoints();
        List<Edge> edges = new ArrayList<>();

        for (int i = 1; i < points.size(); i++) {
            edges.add(new Edge(points.get(i - 1), points.get(i)));
        }

        // Добавление ребра, замыкающего многоугольник
        edges.add(new Edge(points.get(points.size() - 1), points.get(0)));
        polygon.setEdges(edges);
    }

    /**
     * Расчёт коэффициента A уравнения плоскости
     *
     * @param polygon непосредственно прямоугольник
     */
    public void calculateA(Polygon polygon) {
        List<Point> points = polygon.getPoints();
        double result = 0.0;

        for (int i = 0; i < points.size(); i++) {
            result += (points.get(i).getY() - points.get(i + 1).getY()) * (points.get(i).getZ() + points.get(i + 1).getZ());
        }

        result += (points.get(points.size() - 1).getY() - points.get(0).getY())
                * (points.get(points.size() - 1).getZ() + points.get(0).getZ());

        polygon.setA(result);
    }

    /**
     * Расчёт коэффициента B уравнения плоскости
     *
     * @param polygon непосредственно прямоугольник
     */
    public void calculateB(Polygon polygon) {
        List<Point> points = polygon.getPoints();
        double result = 0.0;

        for (int i = 0; i < points.size(); i++) {
            result += (points.get(i).getZ() - points.get(i + 1).getZ()) * (points.get(i).getX() + points.get(i + 1).getX());
        }

        result += (points.get(points.size() - 1).getZ() - points.get(0).getZ())
                * (points.get(points.size() - 1).getX() + points.get(0).getX());

        polygon.setB(result);
    }

    /**
     * Расчёт коэффициента C уравнения плоскости
     *
     * @param polygon непосредственно прямоугольник
     */
    public void calculateC(Polygon polygon) {
        List<Point> points = polygon.getPoints();
        double result = 0.0;

        for (int i = 0; i < points.size(); i++) {
            result += (points.get(i).getX() - points.get(i + 1).getX()) * (points.get(i).getY() + points.get(i + 1).getY());
        }

        result += (points.get(points.size() - 1).getX() - points.get(0).getX())
                * (points.get(points.size() - 1).getY() + points.get(0).getY());

        polygon.setC(result);
    }

    /**
     * Расчёт коэффициента D уравнения плоскости
     *
     * @param polygon непосредственно прямоугольник
     */
    private void calculateD(Polygon polygon) {
        List<Point> points = polygon.getPoints();
        polygon.setD(-(polygon.getA() * points.get(0).getX()
                + polygon.getB() * points.get(0).getY()
                + polygon.getC() * points.get(0).getZ())
        );
    }
}
