# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Turma(models.Model):
    id_turma = models.AutoField(primary_key=True)
    nome_turma = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'turma'

class Aluno(models.Model):
    id_aluno = models.AutoField(primary_key=True)
    nome_aluno = models.CharField(max_length=45)
    datanasc_aluno = models.DateField(db_column='dataNasc_aluno')  # Field name made lowercase.
    cpf_aluno = models.CharField(max_length=11)
    obs_aluno = models.TextField(blank=True, null=True)
    id_turma = models.ForeignKey(Turma, on_delete=models.CASCADE, db_column="id_turma")

    class Meta:
        managed = False
        db_table = 'aluno'


