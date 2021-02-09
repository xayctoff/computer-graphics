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
}
