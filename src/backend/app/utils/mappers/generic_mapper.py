from typing import Any, Dict, List, Optional, Type, Union
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.inspection import inspect
from datetime import datetime

class GenericMapper:
    """
    Mapper genérico universal para modelos SQLAlchemy
    Permite mapear entre modelos, diccionarios y realizar operaciones CRUD
    """
        
    DEFAULT_EXCLUDE_FIELDS = ['id', 'created_at', 'updated_at']
    
    @classmethod
    def map_to_model(cls, source: Union[Dict, Any], target: Any, 
                     exclude_fields: Optional[List[str]] = None,
                     include_none: bool = False) -> Any:
        """
        Mapea datos desde un diccionario o modelo hacia otro modelo
        
        Args:
            source: Diccionario o modelo fuente
            target: Modelo destino
            exclude_fields: Campos a excluir del mapeo
            include_none: Si incluir valores None en el mapeo
        
        Returns:
            El modelo target actualizado
        """
        if exclude_fields is None:
            exclude_fields = cls.DEFAULT_EXCLUDE_FIELDS.copy()
                
        valid_columns = cls._get_model_columns(target)
                
        if isinstance(source, dict):
            return cls._map_dict_to_model(source, target, valid_columns, exclude_fields, include_none)
                
        return cls._map_model_to_model(source, target, valid_columns, exclude_fields, include_none)
    
    @classmethod
    def map_to_dict(cls, model: Any, exclude_fields: Optional[List[str]] = None,
                    include_relationships: bool = False) -> Dict[str, Any]:
        """
        Convierte un modelo SQLAlchemy a diccionario
        
        Args:
            model: Modelo a convertir
            exclude_fields: Campos a excluir
            include_relationships: Si incluir relaciones del modelo
        
        Returns:
            Diccionario con los datos del modelo
        """
        if exclude_fields is None:
            exclude_fields = []
        
        result = {}
                
        for column in cls._get_model_columns(model):
            if column not in exclude_fields:
                value = getattr(model, column, None)                
                if isinstance(value, datetime):
                    value = value.isoformat()
                result[column] = value
                
        if include_relationships:
            for relationship in cls._get_model_relationships(model):
                if relationship not in exclude_fields:
                    related_obj = getattr(model, relationship, None)
                    if related_obj:
                        if hasattr(related_obj, '__iter__') and not isinstance(related_obj, str):                            
                            result[relationship] = [cls.map_to_dict(obj, exclude_fields) for obj in related_obj]
                        else:                            
                            result[relationship] = cls.map_to_dict(related_obj, exclude_fields)
        
        return result
    
    @classmethod
    def create_model(cls, model_class: Type, data: Union[Dict, Any], 
                     exclude_fields: Optional[List[str]] = None) -> Any:
        """
        Crea una nueva instancia del modelo con los datos proporcionados
        
        Args:
            model_class: Clase del modelo a crear
            data: Datos para el nuevo modelo
            exclude_fields: Campos a excluir
        
        Returns:
            Nueva instancia del modelo
        """
        if exclude_fields is None:
            exclude_fields = cls.DEFAULT_EXCLUDE_FIELDS.copy()
                
        new_instance = model_class()
                
        return cls.map_to_model(data, new_instance, exclude_fields)
    
    @classmethod
    def update_model(cls, model: Any, data: Union[Dict, Any], 
                     exclude_fields: Optional[List[str]] = None,
                     partial: bool = True) -> Any:
        """
        Actualiza un modelo existente con nuevos datos
        
        Args:
            model: Modelo a actualizar
            data: Nuevos datos
            exclude_fields: Campos a excluir
            partial: Si es actualización parcial (no incluye None)
        
        Returns:
            Modelo actualizado
        """
        if exclude_fields is None:
            exclude_fields = cls.DEFAULT_EXCLUDE_FIELDS.copy()
        
        return cls.map_to_model(data, model, exclude_fields, include_none=not partial)
    
    @classmethod
    def clone_model(cls, source: Any, exclude_fields: Optional[List[str]] = None) -> Any:
        """
        Clona un modelo (crea una copia sin ID)
        
        Args:
            source: Modelo a clonar
            exclude_fields: Campos adicionales a excluir
        
        Returns:
            Nueva instancia del modelo clonado
        """
        if exclude_fields is None:
            exclude_fields = cls.DEFAULT_EXCLUDE_FIELDS.copy()
        else:
            exclude_fields = cls.DEFAULT_EXCLUDE_FIELDS + exclude_fields
        
        model_class = type(source)
        return cls.create_model(model_class, source, exclude_fields)
    
    @classmethod
    def merge_models(cls, primary: Any, secondary: Any, 
                     exclude_fields: Optional[List[str]] = None,
                     prefer_primary: bool = True) -> Any:
        """
        Mezcla dos modelos, combinando sus datos
        
        Args:
            primary: Modelo principal
            secondary: Modelo secundario
            exclude_fields: Campos a excluir
            prefer_primary: Si preferir valores del modelo primary en caso de conflicto
        
        Returns:
            Modelo primary actualizado con datos merged
        """
        if exclude_fields is None:
            exclude_fields = cls.DEFAULT_EXCLUDE_FIELDS.copy()
        
        valid_columns = cls._get_model_columns(primary)
        
        for column in valid_columns:
            if column not in exclude_fields:
                primary_value = getattr(primary, column, None)
                secondary_value = getattr(secondary, column, None)
                
                if prefer_primary:                    
                    if primary_value is None and secondary_value is not None:
                        setattr(primary, column, secondary_value)
                else:                    
                    if secondary_value is not None:
                        setattr(primary, column, secondary_value)
        
        return primary
        
    @classmethod
    def _get_model_columns(cls, model: Any) -> List[str]:
        """Obtiene las columnas de un modelo SQLAlchemy"""
        if hasattr(model, '__table__'):
            return list(model.__table__.columns.keys())
        return []
    
    @classmethod
    def _get_model_relationships(cls, model: Any) -> List[str]:
        """Obtiene las relaciones de un modelo SQLAlchemy"""
        if hasattr(model, '__mapper__'):
            return [rel.key for rel in inspect(model.__class__).relationships]
        return []
    
    @classmethod
    def _map_dict_to_model(cls, source_dict: Dict, target: Any, 
                          valid_columns: List[str], exclude_fields: List[str],
                          include_none: bool) -> Any:
        """Mapea un diccionario a un modelo"""
        for key, value in source_dict.items():
            if key in valid_columns and key not in exclude_fields:
                if include_none or value is not None:
                    setattr(target, key, value)
        return target
    
    @classmethod
    def _map_model_to_model(cls, source: Any, target: Any, 
                           valid_columns: List[str], exclude_fields: List[str],
                           include_none: bool) -> Any:
        """Mapea un modelo a otro modelo"""
        for column in valid_columns:
            if column not in exclude_fields:
                if hasattr(source, column):
                    value = getattr(source, column, None)
                    if include_none or value is not None:
                        setattr(target, column, value)
        return target