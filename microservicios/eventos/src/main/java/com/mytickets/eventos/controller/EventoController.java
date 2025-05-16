package com.mytickets.eventos.controller;

import com.mytickets.eventos.dto.EventoDTO;
import com.mytickets.eventos.model.Categoria;
import com.mytickets.eventos.model.Evento;
import com.mytickets.eventos.repository.CategoriaRepository;
import com.mytickets.eventos.repository.EventoRepository;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/eventos")
@Tag(name = "Eventos", description = "Operaciones relacionadas con eventos")
public class EventoController {

    private final EventoRepository eventoRepository;
    private final CategoriaRepository categoriaRepository;

    public EventoController(EventoRepository eventoRepository, CategoriaRepository categoriaRepository) {
        this.eventoRepository = eventoRepository;
        this.categoriaRepository = categoriaRepository;
    }

    @PostMapping
    @Operation(summary = "Crear un nuevo evento")
    public ResponseEntity<?> crearEvento(@RequestBody EventoDTO dto) {
        Optional<Categoria> categoriaOpt = categoriaRepository.findById(dto.categoriaId);
        if (categoriaOpt.isEmpty()) {
            return ResponseEntity.badRequest().body("❌ Categoría no encontrada");
        }

        Evento evento = new Evento();
        evento.setNombre(dto.nombre);
        evento.setDescripcion(dto.descripcion);
        evento.setFecha(dto.fecha);
        evento.setLugar(dto.lugar);
        evento.setPrecio(dto.precio);
        evento.setImagen(dto.imagen);
        evento.setCategoria(categoriaOpt.get());

        return ResponseEntity.ok(eventoRepository.save(evento));
    }

    @GetMapping
    @Operation(summary = "Listar todos los eventos")
    public List<Evento> obtenerEventos() {
        return eventoRepository.findAll();
    }
}
