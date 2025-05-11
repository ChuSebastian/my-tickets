package com.mytickets.eventos.controller;

import com.mytickets.eventos.model.Evento;
import com.mytickets.eventos.repository.EventoRepository;
import org.springframework.web.bind.annotation.*;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.List;

@RestController
@RequestMapping("/eventos")
@Tag(name = "Eventos", description = "Operaciones relacionadas con eventos")
public class EventoController {

    private final EventoRepository eventoRepository;

    public EventoController(EventoRepository eventoRepository) {
        this.eventoRepository = eventoRepository;
    }

    @PostMapping
    @Operation(summary = "Crear un nuevo evento")
    public Evento crearEvento(@RequestBody Evento evento) {
        return eventoRepository.save(evento);
    }

    @GetMapping
    @Operation(summary = "Listar todos los eventos")
    public List<Evento> obtenerEventos() {
        return eventoRepository.findAll();
    }
}

