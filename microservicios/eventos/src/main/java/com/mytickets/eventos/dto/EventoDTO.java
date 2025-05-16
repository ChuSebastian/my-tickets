package com.mytickets.eventos.dto;

public class EventoDTO {
    public String nombre;
    public String descripcion;
    public String fecha;
    public String lugar;
    public int precio;
    public String imagen;
    public CategoriaDto categoria;

    public static class CategoriaDto {
        public Long id;
    }
}
